provider "aws" {
  region     = "${var.aws_region}"
  access_key = "${var.aws_access_key}"
  secret_key = "${var.aws_secret_key}"
}

resource "aws_key_pair" "default"{
  key_name = "home"
  public_key = "${file("${var.public_key_path}")}"
}

resource "aws_instance" "load-test" {
  count           = 10
  ami             = "${var.aws_ami}"
  instance_type   = "${var.instance_type}"
  key_name        = "${aws_key_pair.default.id}"
  security_groups = ["launch-wizard-3"]
  tags {
    Name = "bus-${count.index}"
  }
  connection {
    type        = "ssh"
    user        = "${var.user}"
    private_key = "${file("${var.private_key_path}")}"
  }
  provisioner "remote-exec" {
    script = "${var.bootstrap_path}"
  }
  
}
