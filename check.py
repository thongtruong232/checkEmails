import re
import dns.resolver
import smtplib

def is_valid_syntax(email):
    regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return re.match(regex, email) is not None

def check_domain(email):
    domain = email.split('@')[1]
    try:
        dns.resolver.resolve(domain, 'MX')
        return True
    except (dns.resolver.NoAnswer, dns.resolver.NXDOMAIN):
        return False

def check_smtp(email):
    domain = email.split('@')[1]
    try:
        mx_records = dns.resolver.resolve(domain, 'MX')
        mx_record = str(mx_records[0].exchange)

        server = smtplib.SMTP(mx_record)
        server.set_debuglevel(0)
        server.helo(server.local_hostname)  # server.local_hostname(Get local server hostname)
        server.mail('your_email@example.com')
        code, message = server.rcpt(email)
        server.quit()

        if code == 250:
            return True
        else:
            return False
    except Exception as e:
        print(f"An error occurred: {e}")
        return False

def verify_email(email):
    if not is_valid_syntax(email):
        return "Invalid email syntax"
    if not check_domain(email):
        return "Domain does not exist"
    if not check_smtp(email):
        return "Email does not exist"
    return "Email is valid"
def read_txt():
  try:
    with open('emails.txt', 'r', encoding='utf-8') as file:
      content = file.read()
      print(content)
  except FileNotFoundError:
      print("Tệp không tồn tại.")
  except IOError:
      print("Có lỗi khi đọc tệp.")

if __name__ == "__main__":
    try:
      with open('emails.txt', 'r', encoding='utf-8') as file:
        for line in file:
          result = verify_email(line.strip())
          print(result)
          result = result.strip()
          line = line.strip()
          r = line + '||' + result + '\n'
          with open('checkDone.txt','a+', encoding='utf-8') as file:
            file.write(r)

    except FileNotFoundError:
        print("Tệp không tồn tại.")
    except IOError:
        print("Có lỗi khi đọc tệp.")