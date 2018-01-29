import requests
import whois
import datetime
import argparse


def load_urls4check(path):
    with open(path) as urls_list:
        return urls_list.read().split('\n')


def is_server_respond_with_200(url):
    status_is_200 = 200
    return (requests.get(url)).status_code == status_is_200


def get_domain_expiration_date(domain_name):
    month = datetime.datetime.now() + datetime.timedelta(days=30)
    domain = whois.whois(domain_name)
    expiration_date_utc = domain.expiration_date[0]
    return expiration_date_utc > month


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
    return parser.parse_args()


if __name__ == '__main__':
    try:
        args = get_parser_args()
        urls_list = load_urls4check(args.inputfile)
        for url in urls_list:
            status = is_server_respond_with_200(url)
            expiration = get_domain_expiration_date(url)
            print_domains_statuses(url, status, expiration)
    except UnicodeDecodeError:
        print('Incorrect input file')
    except FileNotFoundError:
        print('File not found')
