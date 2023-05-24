from dotenv import load_dotenv
from typing import List
import os

# Load environment variables
load_dotenv()


def get_user_from_file(path: str) -> List:
    # set variables
    user_name, followers, following, posts = 0, 0, 0, 0

    # read input file    
    with open(path, 'r') as f:
        for i,line in enumerate(f):
            if i == 0:
                user_name = line.split(' ')[0]
            else:
                words_in_line = [s.strip() for s in line.split(':')]
                if 'followers' == words_in_line[0].lower():
                    followers = int(words_in_line[1])
                elif 'following' == words_in_line[0].lower():
                    following = int(words_in_line[1])
                elif 'posts' == words_in_line[0].lower():
                    posts = int(words_in_line[1])
    
    # validate read user data
    if f'{user_name}{following}{followers}{posts}' == '0000':
        raise ValueError('Input file was not able to be read. Check schema')

    # if all good,
    return [user_name, followers, following, posts]


def test_get_user_from_data():
    file_path = 'outputs/zkami.txt'
    username, fllw, fllwng, posts = get_user_from_file(file_path)
    assert (username == 'zkami')
    assert (fllw == 1033)
    assert (fllwng == 754)
    assert (posts == 3)
    print('Test : get_user_from_data passed')


if __name__ == "__main__":
    test_get_user_from_data()
