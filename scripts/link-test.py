#!/usr/bin/env python
from __future__ import print_function

import re
import socket
import threading

import paramiko

import common

LOSS_REGEXP = re.compile(r'(\d+) packets transmitted, (\d+) received')
RTT_REGEXP = re.compile(r'rtt min/avg/max/mdev = (.+?)/(.+?)/(.+?)/(.+?) ms')


def push(uuid, link_id, sent, received, rtt_min, rtt_avg, rtt_max):
    print('Link {} : {}%'.format(link_id,100.0 * (1.0 - float(received) / float(sent))))

    """Submit data to nodewatcher instance."""
    body = {
        'sensors.generic': {
            '_meta': {'version': 1},
            'koruza_loss_link_{}'.format(link_id): {
                'name': 'KORUZA Packet Loss (Link {})'.format(link_id),
                'unit': '%',
                'value': 100.0 * (1.0 - float(received) / float(sent)),
            },
            'koruza_rtt_avg_link_{}'.format(link_id): {
                'name': 'KORUZA RTT Average (Link {})'.format(link_id),
                'unit': 'ms',
                'value': float(rtt_avg),
                'group': 'koruza_rtt',
            },
            'koruza_rtt_min_link_{}'.format(link_id): {
                'name': 'KORUZA RTT Min (Link {})'.format(link_id),
                'unit': 'ms',
                'value': float(rtt_min),
                'group': 'koruza_rtt',
            },
            'koruza_rtt_max_link_{}'.format(link_id): {
                'name': 'KORUZA RTT Max (Link {})'.format(link_id),
                'unit': 'ms',
                'value': float(rtt_max),
                'group': 'koruza_rtt',
            },
        }
    }

    common.nodewatcher_push(uuid, body)


def ping(uuid, link_id, source, destination):
    """Ping worker."""
    while True:
        client = paramiko.SSHClient()

        try:
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            client.connect(
                hostname=source,
                username='ubnt',
                password='ubnt',
            )
            stdin, stdout, stderr = client.exec_command('sudo ping -i 0.1 -w 60 -n -q {}'.format(destination))
            results = stdout.read()

            try:
                sent, received = LOSS_REGEXP.findall(results)[0]
            except IndexError:
                continue

            try:
                rtt_min, rtt_avg, rtt_max, rtt_mdev = RTT_REGEXP.findall(results)[0]
            except IndexError:
                rtt_min = 0
                rtt_avg = 0
                rtt_max = 0

            push(uuid, link_id, sent, received, rtt_min, rtt_avg, rtt_max)
        except (paramiko.SSHException, paramiko.SFTPError, socket.error, EOFError):
            continue
        finally:
            client.close()

if __name__ == '__main__':
    print('KORUZA Experiment: Link test script.')

    routers = common.get_config('routers')

    pairs = set()
    for router in routers:
        source_ip = '10.10.{}.1'.format(router['id'])

        for side in ['a', 'b']:
            link_id = router['link_{}'.format(side)]
            if link_id is None:
                continue

            target_router = [
                target
                for target in routers
                if target['id'] != router['id'] and (target['link_a'] == link_id or target['link_b'] == link_id)
            ][0]
            target_ip = '10.20.{}.{}'.format(link_id, target_router['id'])

            uuid = router['uuid_{}'.format(side)]
            pairs.add((uuid, link_id, source_ip, target_ip))

    # Create one thread for each measurement pair.
    threads = []
    for pair in pairs:
        thread = threading.Thread(target=ping, args=pair)
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()
