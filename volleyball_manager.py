<!DOCTYPE html>
<html lang="pl">
<head>
<meta charset="UTF-8">
<title>TV Broadcast Volleyball</title>

<style>

body{
margin:0;
background:black;
font-family:Arial;
color:white;
}

#container{
position:relative;
width:1280px;
margin:auto;
}

canvas{
background:#d9a441;
display:block;
}

#overlay{

position:absolute;
top:0;
left:0;
width:100%;
pointer-events:none;

}

#scoreboard{

background:rgba(0,0,0,0.7);
padding:10px;
font-size:24px;
display:flex;
justify-content:space-between;

}

</style>

</head>

<body>

<div id="container">

<canvas id="game" width="1280" height="600"></canvas>

<div id="overlay">

<div id="scoreboard">

<div>TEAM BLUE <span id="scoreA">0</span></div>

<div>SET <span id="sets">0-0</span></div>

<div><span id="scoreB">0</span> TEAM RED</div>

</div>

</div>

</div>

<script>

const canvas=document.getElementById("game");
const ctx=canvas.getContext("2d");

const scoreA_el=document.getElementById("scoreA");
const scoreB_el=document.getElementById("scoreB");
const sets_el=document.getElementById("sets");

let scoreA=0;
let scoreB=0;

let setsA=0;
let setsB=0;

let cameraX=0;

const NET=640;

class Player{

constructor(x,y,team,name,role){

this.x=x;
this.y=y;

this.team=team;

this.name=name;

this.role=role;

this.jump=0;

}

draw(){

ctx.beginPath();

ctx.arc(this.x-cameraX,this.y-this.jump,14,0,Math.PI*2);

ctx.fillStyle=this.team=="A"?"blue":"red";

ctx.fill();

ctx.fillStyle="white";

ctx.font="12px Arial";

ctx.fillText(this.name,this.x-cameraX-20,this.y-25);

}

jumpAnim(){

this.jump=25;

setTimeout(()=>this.jump=0,300);

}

}

class Ball{

constructor(){

this.x=640;
this.y=300;

this.vx=6;
this.vy=-5;

}

draw(){

ctx.beginPath();

ctx.arc(this.x-cameraX,this.y,8,0,Math.PI*2);

ctx.fillStyle="white";
ctx.fill();

}

update(){

this.x+=this.vx;
this.y+=this.vy;

this.vy+=0.2;

if(this.y>580){

point();

}

}

}

const players=[

new Player(200,150,"A","Kowalski","OH"),
new Player(300,400,"A","Nowak","LIB"),
new Player(400,200,"A","Wiśniewski","SET"),

new Player(1000,150,"B","Smith","OH"),
new Player(900,400,"B","Jones","LIB"),
new Player(800,200,"B","Brown","SET"),

];

const ball=new Ball();

function drawCourt(){

ctx.fillStyle="white";

ctx.fillRect(NET-cameraX,0,5,600);

}

function updateScore(){

scoreA_el.innerText=scoreA;
scoreB_el.innerText=scoreB;

sets_el.innerText=setsA+"-"+setsB;

}

function camera(){

cameraX=ball.x-640;

}

function rally(){

players.forEach(p=>{

if(Math.random()<0.01){

p.jumpAnim();

}

});

}

function point(){

if(ball.x<NET){

scoreB++;

}else{

scoreA++;

}

updateScore();

ball.x=640;
ball.y=300;

}

function update(){

ctx.clearRect(0,0,1280,600);

camera();

drawCourt();

players.forEach(p=>p.draw());

ball.draw();

ball.update();

rally();

requestAnimationFrame(update);

}

updateScore();

update();

</script>

</body>
</html>
