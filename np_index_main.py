from Index.non_positional.Index import Index
from utils.utils import Utils

if __name__ == '__main__':
    obj = Index()
    obj.create_index()
    obj.save_index_to_file()