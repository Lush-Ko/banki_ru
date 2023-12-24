import yaml

from src import gigachat_process, preproc_reviews, get_clusters, learn_clusters


def execute(args):
    preproc_reviews.preproc_reviews(args)
    gigachat_process.gigachat_process(args)
    learn_clusters.make_clusters(args)
    get_clusters.calculate_data(args)


def main():
    with open("data/config.yaml", "r", encoding='utf-8') as stream:
        args = yaml.safe_load(stream)['config_data']

    execute(args)


if __name__ == "__main__":
    main()
