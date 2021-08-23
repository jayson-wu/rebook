from sys import stdin

def main():
    str = '''
    Content-type: Text/html
    <!DOCTYPE html>
    ’<html>
    ’<body>
    '''
    print(str)
    value = stdin.readline()
    while (value is not None):
        print(value)
        value = stdin.readLine()
    print('</body>')
    print('</html>')


if __name__ == '__main__':
    main()