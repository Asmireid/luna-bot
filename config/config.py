import codecs
import configparser


def load_config():
    # Read the configuration file
    with codecs.open('config/config.ini', 'r', encoding='utf-8') as f:
        configurations = configparser.ConfigParser()
        configurations.read_file(f)
    return configurations


configs = load_config()


def bot_token(): return configs.get('credentials', 'bot_token')
def bot_name(): return configs.get('customizations', 'bot_name')
def bot_activity(): return configs.get('customizations', 'bot_activity')
def embed_footer(): return configs.get('customizations', 'embed_footer')
def command_prefix(): return configs.get('settings', 'command_prefix')
def display_confirmation(): return configs.getboolean('settings', 'display_confirmation')
def delete_confirmation(): return configs.getboolean('settings', 'delete_confirmation')
def wait_time(): return configs.getint('settings', 'seconds_before_deleting_confirmation')
def reply(): return configs.getboolean('settings', 'reply')
def mention_author(): return configs.getboolean('settings', 'mention_author')
def delete_invocation(): return configs.getboolean('settings', 'delete_invocation')
def ephemeral(): return configs.getboolean('settings', 'ephemeral')
