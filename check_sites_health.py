import requests
import whois
import datetime
import argparse


def get_urls4check(path):
    with open(path) as urls_list:
        return urls_list.read().split('\n')


def is_domain_paid(domain_name, days):
    number_of_days = datetime.datetime.now() + datetime.timedelta(days=days)
    domain_info = whois.whois(domain_name)
    try:
        expiration_date_utc = domain_info.expiration_date[0]
    except TypeError:
        expiration_date_utc = domain_info.expiration_date
    finally:
        if not expiration_date_utc:
            return False
        else:
            return expiration_date_utc > number_of_days


def print_domains_statuses(url, status, expiration):
    if status and expiration:
        print('{} is active and paid'.format(url))
    elif not status:
        print('{} is not available'.format(url))
    elif not expiration:
        print('{} is not paid'.format(url))


def get_parser_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-i', '--inputfile',
        help='Path to txt file with list of domains. Required parameter',
        required=True
    )
    parser.add_argument(
        '-d', '--days',
        help='Check if domain payment ends in specified number of days. '
             'Default 30 days',
        default=30,
        type=int
    )
    return parser.parse_args()


if __name__ == '__main__':
    try:
        args = get_parser_args()
        urls_list = get_urls4check(args.inputfile)
        for url in urls_list:
            status = requests.get(url).ok
            expiration = is_domain_paid(url, args.days)
            print_domains_statuses(url, status, expiration)
    except UnicodeDecodeError:
        print('Incorrect input file')
    except FileNotFoundError:
        print('File not found')
