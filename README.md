# Kindle_Export
## App
![](https://s3.us-west-2.amazonaws.com/secure.notion-static.com/3f4f1d79-145d-4fa1-8b5f-2441724b9ad0/Untitled.png?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIAT73L2G45O3KS52Y5%2F20210428%2Fus-west-2%2Fs3%2Faws4_request&X-Amz-Date=20210428T060801Z&X-Amz-Expires=86400&X-Amz-Signature=0e8fc5c1fe1c03d10c782c61ee804e14158512d5ed02f866265a9ea3f165287f&X-Amz-SignedHeaders=host&response-content-disposition=filename%20%3D%22Untitled.png%22)

[Kindle Highlight Export to Notion](https://kindle-export.herokuapp.com/)

## Uploading Higlights text file

- Connect your kindle to your computer by wire.
- Go inside documents folder and find My_clippings.txt file there.
- Upload this file to file field

## Getting `token_v2`

### Firefox :

1. Press Ctrl+Shift+I or open Applications menu on the right, expand Web Developer and click Web Developer Tools (as shown).
2. This opens up Web Developer Tools. 
3. Now open `Storage` tab on top and click on [notion.so](http://notion.so) cookies on the left. You will find token_v2 cookie here.
4. Double click on it's value and copy it and paste it inside token_v2 field.

### Chrome

1. Similarly press Ctrl+Shift+I on chrome as well.
2. Go to Application tab and find Cookies tab on the left.
3. Click on [notion.so](http://notion.so) cookies.
4. Find token_v2 cookie and double click on it's value and copy it and paste it inside token_v2 field.
## Table Link

1. Make a new notion page. Now press the table option when prompted with options for the new page
2. Now on the top-right corner, click on Share button. Enable Share to Web and also allow editing, allow comments and allow duplicate as template. **This is very important and highlights cannot be imported if this is not done.**
3. Now press on 3 horizontal dots on the top-right corner of table and select Copy Link to view.
4. Paste this value to the Notion Table URL field.

## That's it!

- The highlights will automatically be added to your Notion Account.
- This may take some time, so don't disturb it. After the process is finished, you can make your page private!
