provider "aws" {
  region = "us-east-1"
}

resource "aws_vpc" "kalki_vpc" {
  cidr_block           = "10.0.0.0/16"
  enable_dns_hostnames = true
  enable_dns_support   = true
  tags = {
    Name = "kalki-vpc"
  }
}

resource "aws_subnet" "kalki_subnet_1" {
  vpc_id            = aws_vpc.kalki_vpc.id
  cidr_block        = "10.0.1.0/24"
  availability_zone = "us-east-1a"
}

resource "aws_subnet" "kalki_subnet_2" {
  vpc_id            = aws_vpc.kalki_vpc.id
  cidr_block        = "10.0.2.0/24"
  availability_zone = "us-east-1b"
}

resource "aws_eks_cluster" "kalki_eks" {
  name     = "kalki-eks-cluster"
  role_arn = aws_iam_role.kalki_eks_role.arn

  vpc_config {
    subnet_ids = [aws_subnet.kalki_subnet_1.id, aws_subnet.kalki_subnet_2.id]
  }
}

resource "aws_iam_role" "kalki_eks_role" {
  name = "kalki-eks-cluster-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Action = "sts:AssumeRole"
      Effect = "Allow"
      Principal = {
        Service = "eks.amazonaws.com"
      }
    }]
  })
}

resource "aws_db_instance" "kalki_rds" {
  allocated_storage   = 20
  engine              = "postgres"
  engine_version      = "16"
  instance_class      = "db.t4g.micro"
  db_name             = "kalki_db"
  username            = "postgres"
  password            = "postgrespassword"
  skip_final_snapshot = true
}
