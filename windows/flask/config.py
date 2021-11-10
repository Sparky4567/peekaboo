from chromedriver_py import binary_path
base_name="datastore"
admin_base_name="admintable"
peek_prefix="https://"
peekaboo_admin="test"
peekaboo_password="test"
db_prefix=".db"
peekaboo_agent="Peekaboo-Prerender"
webdriver_path=binary_path
peekaboo_ip="127.0.0.1"
peekaboo_port="8000"
eliminate_links = ["script", "style","iframe","link"]
eliminate_tags = ["class", "id", "name", "style"]
selenium_timeout = 3
helper_route_enabled = True

#Redis
redis_support_enabled = True
redis_host = "localhost"
redis_port = 6379
redis_db = 0