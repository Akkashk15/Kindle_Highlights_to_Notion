const express=require("express");
const app=express();
const methodOverride=require("method-override");
const ejsMate=require("ejs-mate");
const path=require("path");
const upload=require("express-fileupload");
const {v4 : uuidv4} = require('uuid')
const spawn = require("child_process").spawn;



app.use(methodOverride("_method"));
app.use(express.urlencoded({extended:true}));
app.engine("ejs",ejsMate);
app.set("view engine","ejs");

// Middleware
app.use(upload());


app.get("/",function(req,res){
    res.render("home.ejs");
});

app.post("/",function(req,res){
    if(req.files){
        var file = req.files.filename;
        var filename=uuidv4()+file.name;
        var token_v2=req.body.notionToken;
        var table_link=req.body.tableLink;

        file.mv("./uploads/"+filename,function(err){
            if(err){
                res.send(err);
            } 
            else{
                // Send data to Notion API here from file
                res.render("welcome.ejs");
                const pythonProcess = spawn('python',["./txt.py", filename,token_v2,table_link]);
            }
        });
    }
    else{
      res.render("error.ejs");
    }
});

//ERROR
app.all("*",function(req,res,next){
    res.send("Looks like you are lost!");
});

const port=process.env.PORT || 5000;
app.listen(port,function(){
    console.log("Server is online");
});