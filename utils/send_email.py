from dataclasses import dataclass, field, astuple

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from pathlib import Path


@dataclass
class SendEmailConfig:
	smtp_server: str
	port: int
	from_addr: str
	to_addr: str
	username: str
	password: str
	subject: str
	text: str
	filename_list: list[Path] = field(default_factory=list)


def send_email(config: SendEmailConfig) -> None:
	smtp_server, port, from_addr, to_addr, username, password, subject, text, filename_list = astuple(config)

	# 创建MIMEMultipart对象，用于存储邮件内容
	msg = MIMEMultipart()

	# 创建MIMEText对象，将文本内容添加到MIMEMultipart对象中
	text_part = MIMEText(text)
	msg.attach(text_part)
	for filename in filename_list:
		# 构造附件
		with open(str(filename), "rb") as f:
			# 创建MIMEApplication对象，将附件添加到MIMEMultipart对象中
			attachment_part = MIMEApplication(f.read())
			attachment_part.add_header("Content-Disposition", "attachment", filename=filename.name)
			msg.attach(attachment_part)

	# 设置邮件主题、发件人和收件人
	msg["Subject"] = subject
	msg["From"] = from_addr
	msg["To"] = to_addr

	# 创建SMTP对象，连接SMTP服务器
	with smtplib.SMTP(smtp_server, port) as server:
		server.starttls()
		# 登录SMTP服务器
		server.login(username, password)
		# 发送邮件
		server.sendmail(from_addr, [to_addr], msg.as_string())

	print("邮件发送成功！")
