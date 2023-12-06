# Orders System API

![Tests](https://github.com/jahlon/orders-system/workflows/test-and-lint.yml/badge.svg)
![CodeQL](https://github.com/jahlon/orders-system/workflows/codeql-analysis.yml/badge.svg)
![Coverage](https://jahlon.github.io/orders-system/coverage.svg)

## Description
Orders System API simulates a simple order management system. 
It allows you to create, update, delete and get orders and products.
It is intended to be used as a sample project for learning design patterns and principles to
design and implement maintainable and reusable software.

## Instructions for cloning or forking this repository
If you want to clone or fork this repository, bear in mind the following:

1. you need to create a **.env** file in your own environment. You can use 
the **.env_template** file as a template.
2. Product images are stored in a AWS S3 bucket. You need to create a bucket and
set the AWS credentials in the **.env** file.
3. You need to define a KEY in the **.env** file. This key will be used to encrypt
and decrypt the JWT token.