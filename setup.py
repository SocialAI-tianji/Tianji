from setuptools import setup, find_packages

setup(
    name="tianji",
    version="1.2.0",
    description="天机是一个免费的非商业人工智能系统，旨在提升情感智能和核心竞争力。",
    author="SocialAI",
    url="https://socialai-tianji.github.io/socialai-web/",
    packages=find_packages(exclude=["build", "dist"]),
    install_requires=[
        "metagpt==0.6.0" "transformers==4.36.2",
        "sentencepiece==0.1.99",
        "accelerate==0.24.1",
        "transformers_stream_generator==0.0.4",
        "modelscope",
        "tiktoken",
        "einops",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
)
