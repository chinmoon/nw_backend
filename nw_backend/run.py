from app import app

if __name__ == '__main__':
    print("\nRegistered Routes:")
    for rule in app.url_map.iter_rules():
        if 'swagger' in str(rule) or '_openapi' in str(rule):
            print(f"{rule.endpoint}: {rule.rule}")
    app.run(host="127.0.0.1", port=8080, debug=True)