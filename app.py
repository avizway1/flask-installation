from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Sample data for demonstration purposes
posts = [
    {'title': 'First Post', 'content': 'This is the content of the first post.'},
    {'title': 'Second Post', 'content': 'Another interesting post goes here.'}
]

@app.route('/')
def home():
    return render_template('index.html', title='Home', posts=posts)

@app.route('/post/<int:index>')
def show_post(index):
    if 0 <= index < len(posts):
        post = posts[index]
        return render_template('post.html', title=post['title'], post=post)
    else:
        return render_template('not_found.html', title='Not Found'), 404

@app.route('/new_post', methods=['GET', 'POST'])
def new_post():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        new_post = {'title': title, 'content': content}
        posts.append(new_post)
        return redirect(url_for('home'))
    return render_template('new_post.html', title='New Post')

# Route to render not_found.html
@app.errorhandler(404)
def not_found(e):
    return render_template('not_found.html', title='Not Found'), 404

if __name__ == '__main__':
    app.run(debug=True)

