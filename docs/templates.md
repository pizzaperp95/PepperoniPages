# Templates

Making a template is pretty simple. Just make an HTML document however you would normally, but where you want your content to go, you add ```<pepperonipages>```. That tag will be replaced by the contents of your page.
Also include ```<peppages-head>``` in the head of your document.

Example:

```html
<!DOCTYPE html>


<html>
<head>
    <link rel="stylesheet" href="/style.css">
    <peppages-head>
<body>
    <p>Template!!!</p>
        <pepperonipages> <!-- this is where your content will go. -->
    <p>Goodbye. :)</p>
</body>
</head>
</html>
```


