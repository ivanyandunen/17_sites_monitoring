import requests
import whois
import datetime
import argparse


def get_urls4check(path):
    with open(path) as urls_list:
        return urls_list.read().split('\n')


def is_server_respond_with_200(url):
    ok_status = 200
    return requests.get(url).status_code == ok_status


def get_domain_expiration_date(domain_name, days):
    number_of_days = datetime.datetime.now() + datetime.timedelta(days=days)
    domain = whois.whois(domain_name)
    try:
        expiration_date_utc = domain.expiration_date[0]
    except TypeError:
        expiration_date_utc = domain.expiration_date
    finally:
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
            status = is_server_respond_with_200(url)
            expiration = get_domain_expiration_date(url, args.days)
            print_domains_statuses(url, status, expiration)
    except UnicodeDecodeError:
        print('Incorrect input file')
    except FileNotFoundError:
        print('File not found')
