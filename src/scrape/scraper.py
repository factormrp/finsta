from aiohttp import web, ClientSession
from typing import List
from time import sleep
import argparse as ap
import asyncio as aio
import sys
import os


async def get_user_url(username: str) -> str:
    return f'https://www.instagram.com/{username}/?__a=1'


async def fetch_user_data(username: str) -> str:
    """Query Instagram endpoint that returns user meta data"""
    user_url = await get_user_url(username)
    async with ClientSession() as session:
        async with session.get(user_url) as res:
            return await res.text()


def _write_to_file(body: str, path: str, mode: str = 'w') -> None:
    if mode.lower() in ['w','a']:
        with open(path, mode) as f:
            f.write(body)


def to_html(body: str, path: str, mode: str = 'w') -> None:
    _write_to_file(body, path, mode)


def to_txt(body: str, path: str, mode: str = 'w') -> None:
    _write_to_file(body, path, mode)


def read_html(path: str) -> str:
    with open(path, 'r') as f:
        return f.read()


async def get_user_meta_data(
    path: str = None, 
    user_data: str = None
) -> List[str]:
    # Get data, either by reading pre-downloaded file or given data
    if path is not None and user_data is None:
        lines = read_html(path)
    elif path is None and user_data is not None:
        lines = user_data
    else:
        lines = "test\ntest"

    # return cleaned line
    cleaned = lines[:10000].split(">")
    for line in cleaned:
        if "meta content" in line:
            splits = [i for i in [
                ''.join(filter(str.isdigit, num.strip()))
                for num in line[15:line.index('- See')].split(' ')
            ] if i != '']
            return splits


async def main(args: ap.Namespace, user: str) -> None:
    # Define path where user data is expected to live
    path = os.path.join('users', f'{user}.html')

    # If file exists, use it 
    if os.path.exists(path):
        followers, following, posts = await get_user_meta_data(path=path)
    else: # Otherwise fetch it
        raw_data = await fetch_user_data(user)
        if args.download:
            to_html(raw_data, path)
        try:
            followers, following, posts = await get_user_meta_data(
                user_data=raw_data
            )
        except TypeError:
            try:
                followers, following, posts = await get_user_meta_data(
                    user_data=raw_data
                )
            except TypeError:
                to_txt("Could not fetch {user} metadata\n","error.txt", 'a')
                return

    # Report meta_data
    report = f'{user} User Stats:\n------------------\n\tFollowers:\t' \
        f'{followers}\n\tFollowing:\t{following}\n\tPosts:\t\t{posts}'
    if args.output:
        to_txt(report, os.path.join('outputs', f'{user}.txt'))


if __name__ == '__main__':
    # Parse commandline arguments
    parser = ap.ArgumentParser()
    # parser.add_argument("user",action='store')
    parser.add_argument("-d","--download",action='store_true')
    parser.add_argument("-o","--output",action='store_true')
    args = parser.parse_args(sys.argv[1:])

    # Identify path to usernames file and read it
    path = os.path.join('users', 'usernames.txt')
    with open(path, 'r') as f:
        usernames = f.read()

    # For each user, scrape meta data
    for user in usernames.split('\n'):
        # Run top-level closure on main
        aio.run(main(args, user))
