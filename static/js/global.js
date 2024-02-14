docLink = document.createElement('div');
docLink.innerHTML = '<a href="{% url "doc" %}" target="_blank">Psst! ... BRE Documentation</a>';
docLink.style.position = 'sticky';
docLink.style.right = 0;
docLink.style.bottom = 0;
docLink.style.width = 'max-content';
docLink.style.backgroundColor = '#eaeaea';
docLink.style.padding = '.4rem';
docLink.style.border = '1px solid black';

document.body.style.minHeight = '100vh'
document.body.appendChild(docLink)