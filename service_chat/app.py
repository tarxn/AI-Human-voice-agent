from jina import Deployment
from executor import TokenStreamingExecutor

if __name__ == "__main__":
    with Deployment(uses=TokenStreamingExecutor, port=12345, protocol='grpc') as dep:
        dep.block()
