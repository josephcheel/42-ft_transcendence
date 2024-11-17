import express from 'express';
import { createServer } from 'https';
// import { createServer } from 'http';
import { Server } from 'socket.io';
import { dirname } from 'path';
import path from 'path';
import crypto from 'crypto';
import { instrument } from '@socket.io/admin-ui';
import cors from 'cors';
import cookieParser from 'cookie-parser';
import cookie from 'cookie';
import fs from 'fs';
import { fileURLToPath } from 'url';
/* VARIABLES */
const MAX_GOALS = 5;
const MAX_SPEED = 70;

const sleep = async (ms)  => {
    await new Promise(resolve => {
      return setTimeout(resolve, ms);
    });
  };
class Vector3 {
    constructor(x, y, z)
    {
        this.x = x;
        this.y = y;
        this.z = z;
    }
    clone()
    {
        return new Vector3(this.x, this.y, this.z);
    }
    add(vector)
    {
        this.x += vector.x;
        this.y += vector.y;
        this.z += vector.z;
        return this;
    }
    sub(vector)
    {
        this.x -= vector.x;
        this.y -= vector.y;
        this.z -= vector.z;
        return this;
    }
    multiplyScalar(scalar)
    {
        this.x *= scalar;
        this.y *= scalar;
        this.z *= scalar;
        return this;
    }
    copy(vector)
    {
        this.x = vector.x;
        this.y = vector.y;
        this.z = vector.z;
    }
    clamp(min, max)
    {
        // Manually clamp each component (x, y, z) of the sphere position
        this.x = Math.max(min.x, Math.min(this.x, max.x));
        this.y = Math.max(min.y, Math.min(this.y, max.y));
        this.z = Math.max(min.z, Math.min(this.z, max.z));
    }

    distanceTo(vector)
    {
        const dx = vector.x - this.x;
        const dy = vector.y - this.y;
        const dz = vector.z - this.z;
        return Math.sqrt(dx * dx + dy * dy + dz * dz);
    }
    
}

class UserInput {
    constructor()
    {
        this.up = false;
        this.down = false;   
    }
}
class Ball extends UserInput {
    constructor(position, velocity)
    {
        super();

        this.velocity = velocity instanceof Vector3 ? velocity : new Vector3(velocity);
        this.speed = 25;
        this.radius = 1;
        this.position = position;
        this.velocity.multiplyScalar(this.speed);
        this.isGoal = false;
        this.boundaries = { x: 50, y: 25 };
        this.score = { player1: 0, player2: 0 };
        this.finished = false;
    }
    async update(deltaTime) {
        const displacement = this.velocity.clone().multiplyScalar(deltaTime);
        const newPosition = this.position.clone().add(displacement);
        
        // Check boundaries
        if (Math.abs(newPosition.x) > this.boundaries.x - this.radius && !this.isGoal) {
            // Ball hit left or right wall
            // console.log('Goal');
            // console.log('Position:', newPosition);
            // console.log('room:', this.room);
            if (newPosition.x > 0)
            {
                this.score.player1++;
                if (this.score.player1 === MAX_GOALS)
                {
                    io.to(this.room).emit('endGame', 1);
                    io.to(this.room).emit('closeTheGame');
                    io.to(this.room).socketsLeave(this.room);
                    let winner =  { username: undefined, points: 0 };
                    let loser = { username: undefined, points: 0 };
                    for (let id in players)
                    {
                        if (players[id].room == this.room)
                        {
                            console.log('player1')
                            console.log(players[id]);
                            if (players[id].nb == 2)
                            {
                                winner.username = players[id].username;
                                winner.points = this.score.player1;
                            }
                            else
                            {
                                loser.username   = players[id].username;
                                loser.points = this.score.player2;
                            }
                            delete players[id];
                        }
                    }
                    console.log('API CALL', {winner, loser} );
                    this.finished = true;
                }
                else
                    io.to(this.room).emit('goal_scored',{PlayerNb: 1,score: this.score });
            }
            else
            {    
                this.score.player2++;
                if (this.score.player2 === MAX_GOALS)
                {
                    io.to(this.room).emit('endGame', 2);
                    io.to(this.room).emit('closeTheGame');
                    io.to(this.room).socketsLeave(this.room);
                    let winner =  { username: undefined, points: 0 };
                    let loser = { username: undefined, points: 0 };
                    for (let id in players)
                    {
                        if (players[id].room == this.room)
                        {
                            console.log('player2')
                            console.log(players[id]);
                            if (players[id].nb == 1)
                            {
                                winner.username = players[id].username;
                                winner.points = this.score.player2;
                            }
                            else
                            {
                                loser.username   = players[id].username;
                                loser.points = this.score.player1;
                            }
                            delete players[id];
                        }
                    }
                    // let json = {winner: winner.username, looser: loser.username, winner_points: winner.points, looser_points: loser.points};
                    // let response = axios.post(`https://${ORIGIN_IP}:8000/api/tournaments/match_finish`, json);
                    // if (response.status === 200)
                    // {
                    //     console.log('200', { response });
                    // }
                    console.log('API CALL', {winner, loser});
                    this.finished = true;
                }
                else
                io.to(this.room).emit('goal_scored', {PlayerNb: 2,score: this.score });
            }
            this.isGoal = true;
            setTimeout(() => {
                newPosition.x = 0;
                newPosition.y = 0;
                newPosition.z = 0;
                this.velocity.x *= -1;
                this.speed 
                this.isGoal = false;
                this.position.copy(newPosition);
                io.to(this.room).emit('continue_after_goal');
            }, 2000);
        }

        if (Math.abs(newPosition.z) > this.boundaries.y - this.radius) {
            // Ball hit top or bottom wall
            this.velocity.z *= -1;
            newPosition.z = Math.sign(newPosition.z) * (this.boundaries.y - this.radius);
            if (this.room !== undefined)
                io.to(this.room).emit('colision-wall');
        }

        this.position.copy(newPosition);
    }
}

class Paddle extends UserInput {
    constructor(position, width, height, depth)
    {
        super();

        this.position = position;
        this.width = width;
        this.height = height;
        this.depth = depth
        this.score = 0;
        this.room = undefined;
        this.isWaiting = false;
        this.id = undefined;
        this.keySpeed = 0.9;
        this.nb = undefined;
        this.connected = true;
        this.matchId = null;
        this.tournamentId = null;
        this.username = undefined;
        this.ball = undefined;
    }

    PaddleLimits() {
        if (this.position.z > 22)
            this.position.z = 22;
        else if (this.position.z < -22)
            this.position.z = -22;
    }

    keyHandler()
    {
        if (this.down)
            this.position.z +=  this.keySpeed; 
        else if (this.up)
            this.position.z -=  this.keySpeed;
    }
    handleCollision(ball) {
        const paddleLeft = this.position.x - this.width / 2;
        const paddleRight = this.position.x + this.width / 2;
        const paddleTop = this.position.z + this.depth / 2;
        const paddleBottom = this.position.z - this.depth / 2;
    
        if (ball.position.x - ball.radius <= paddleRight &&
            ball.position.x + ball.radius >= paddleLeft &&
            ball.position.z - ball.radius <= paddleTop &&
            ball.position.z + ball.radius >= paddleBottom) {
            
            // Determine collision side
            if (Math.abs(ball.position.x - paddleLeft) < ball.radius || 
                Math.abs(ball.position.x - paddleRight) < ball.radius) {
                    io.to(this.room).emit('colision-paddle');
                this.ball.velocity *= 10;
                return 1; // Collision on X-axis
            } else {
                
                io.to(this.room).emit('colision-paddle');
                console.log(this.ball)
                this.ball.velocity *= 10;
                console.log(this.ball)
                return 2; // Collision on Z-axis
            }
        }
    
        return 0; // No collision
    }
    
    handleCollision4(ball) {
        const paddleLeft = this.position.x - this.width / 2;
        const paddleRight = this.position.x + this.width / 2;
        const paddleTop = this.position.z + this.depth / 2;
        const paddleBottom = this.position.z - this.depth / 2;
    
        const ballLeft = ball.position.x - ball.radius;
        const ballRight = ball.position.x + ball.radius;
        const ballTop = ball.position.z + ball.radius;
        const ballBottom = ball.position.z - ball.radius;
    
        // Check for collision
        if (ballLeft <= paddleRight && ballRight >= paddleLeft &&
            ballBottom <= paddleTop && ballTop >= paddleBottom) {
            
            // Calculate the overlap on both axes
            const overlapX = Math.min(ballRight - paddleLeft, paddleRight - ballLeft);
            const overlapZ = Math.min(ballTop - paddleBottom, paddleTop - ballBottom);
    
            // Determine collision side based on the smaller overlap
            if (overlapX < overlapZ) {
                this.ball.ball.velocity.multiplyScalar(-1);
                this.ball.ball.velocity.multiplyScalar(1.5);
                // Collision on X-axis
                return 1; // Collision on X-axis
            } else {
                console.log(this.ball)
                this.ball.ball.velocity.multiplyScalar(-1);
                this.ball.ball.velocity.multiplyScalar(1.5);
                // Collision on Z-axis
                return 2; // Collision on Z-axis
            }
        }
    
        return 0; // No collision
    }       
}

const port = 4000;

const app = express();
const ORIGIN_IP = process.env.ORIGIN_IP || 'localhost';
console.log('ORIGIN_IP:', ORIGIN_IP);

app.use(cors({
    origin: ["https://admin.socket.io", `http://${ORIGIN_IP}:5173`, `http://${ORIGIN_IP}:5174`, `https://${ORIGIN_IP}:8000`, 'https://miniature-journey-9gr5x5gxwvjfxqv-5173.app.github.dev'],
    credentials: true
}));

// app.use(cors({
//     origin: "*",
//     // credentials: true
// }));


const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

// Load the SSL certificates
const pemFilePath = path.join(__dirname, 'selfsigned.crt');
const keyFilePath = path.join(__dirname, 'selfsigned.key');

// Read the files
const serverOptions = {
    key: fs.readFileSync(keyFilePath),
    cert: fs.readFileSync(pemFilePath),
};

const server = createServer(serverOptions, app);

const io = new Server(server, {
    cors: {
        // origin: "*", 
        origin: ["https://admin.socket.io", `http://${ORIGIN_IP}:5173`, `http://${ORIGIN_IP}:5174`, `https://${ORIGIN_IP}:8000`, 'https://miniature-journey-9gr5x5gxwvjfxqv-5173.app.github.dev'],
        credentials: true
    },
    pingInterval: 2000, pingTimeout: 5000,
});

var players = {};
var balls = {};
var positions = {};
const centerDistanceToPaddle = 45;


let s = false;
let lastTickTime = Date.now();

function GameLoop()
{
    const currentTime = Date.now();
    const deltaTime = (currentTime - lastTickTime) / 1000; // Time difference in seconds
    lastTickTime = currentTime;
    // console.log('Game Loop', Object.keys(players).length);
    for (let playerId in players)
        {
            players[playerId].keyHandler();
            players[playerId].PaddleLimits();
    
            if (balls[players[playerId].room])
            {
                switch (players[playerId].handleCollision4(balls[players[playerId].room].ball))
                {
                    case 1:
                        // balls[players[playerId].room].ball.velocity.x *= -1;
                        // balls[players[playerId].room].ball.velocity.multiplyScalar(10);
                        // balls[pl]
                        break;
                    case 2:
                        // balls[players[playerId].room].ball.velocity.z *= -1;
                        // balls[players[playerId].room].ball.velocity.multiplyScalar(10);
                        break;
                }
            }
            io.to(players[playerId].room).emit('updatePlayer', { id: playerId , z: players[playerId].position.z, nb: players[playerId].nb });
    }       
    for (let id in balls)
    {
        if (balls[id].ball.finished == true)
        {
            // console.log('Game Finished');
            delete balls[id];
            continue
        }
        balls[id].ball.update(deltaTime);
        io.to(id).emit('updateBall', balls[id].ball.position);
    }
}

setInterval(GameLoop, 15);

function setCookie(socket) {
    const roomIdCookie = {
        name: 'roomId',
        value: players[socket.id].room,
        options: { 
            path: '/', 
            expires: new Date(Date.now() + 240000).toUTCString(),
            sameSite: 'None', 
            secure: true 
        }
    };
    io.to(players[socket.id].room).emit('set-cookie', [roomIdCookie]);
}

async function startCountdown(room, player1, player2) {
    // console.log('Start Countdown');

    // await sleep(1000);
    io.to(room).emit('countdown-3', {player1: players[player1], player2: players[player2]});
    await sleep(1000);
    io.to(room).emit('countdown-2');
    await sleep(1000);
    io.to(room).emit('countdown-1');
    await sleep(1000);
    io.to(room).emit('countdown-GO');
    await sleep(1000);
    io.to(room).emit('countdown-end');
  }
  
async function startGame(room, socketId, KeyPlayer1) {
    await startCountdown(room, socketId, KeyPlayer1);
    balls[room].ball.velocity = new Vector3(1, 0, (Math.random() * 1).toFixed(2)).multiplyScalar(balls[room].ball.speed);
    io.to(room).emit('startGame', { player1: players[socketId], player2: players[KeyPlayer1], ball: balls[room] });
}

io.on("connection", (socket) => {
    console.log('New Connection');
    // const username = localStorage.getItem('username');
    // console.log('Username:', username);
    let reconnected = false
    const cookiesHeader = socket.handshake.headers.cookie;
    if (cookiesHeader)
    {  
        // console.log('THere are cookies');
        // console.log('Cookies:', cookiesHeader);
        const cookies = cookie.parse(cookiesHeader);
        // Add username by the COOKIE SESSIONID
        if (cookies.playerId && cookies.roomId)//&& io.sockets.adapter.rooms.has(cookies.roomId)) // Problem if the two players disconnect could never reconnect again, but if I uncomment 'io.sockets.adapter.rooms.has(cookies.roomId)' then you can create a game with yourself just recharging the page
        { 
            // console.log('PlayerId:', cookies.playerId);
            if (players[cookies.playerId] && players[cookies.playerId].connected === false)
            {
                reconnected = true;
                players[cookies.playerId].id = socket.id
                players[cookies.playerId].connected = true;
                players[socket.id] = players[cookies.playerId];
                socket.join(cookies.roomId);
                setCookie(socket);
                console.log('Reconnected:', socket.id);
                
                delete players[cookies.playerId]
                if (players[socket.id].nb == 1)
                {
                    const playerTwo = Object.values(players).find(player => player.room === cookies.roomId && player.nb === 2);
                    io.to(cookies.roomId).emit('reconnect', { player1: players[socket.id], player2: playerTwo, score: balls[cookies.roomId].ball.score, nb: players[socket.id].nb });
                }
                else
                {
                    const playerOne = Object.values(players).find(player => player.room === cookies.roomId && player.nb === 1);
                    io.to(cookies.roomId).emit('reconnect', { player2: players[socket.id], player1: playerOne, score: balls[cookies.roomId].ball.score, nb: players[socket.id].nb });
                }
            }
        }
    }
    if (reconnected == false)
    {
        const query = socket.handshake.query;
        const matchId = query["match-id"] || null;
        const tournamentId = query['tournament-id'] || null;
        const username = query['username'] || null;
        
        players[socket.id] = new Paddle(new Vector3(0, 0, 0), 1, 2, 6);
        players[socket.id].id = socket.id;
        players[socket.id].matchId = matchId;
        players[socket.id].tournamentId = tournamentId;
        players[socket.id].username = username;

        let pairedPlayerId = null;
        for (let id in players) {
            if (id !== socket.id) {
                const otherPlayer = players[id];
                if (otherPlayer.isWaiting && otherPlayer.matchId === matchId && otherPlayer.tournamentId === tournamentId) {
                    pairedPlayerId = id;
                    break;
                }
            }
        }

        if (pairedPlayerId) {
            // Pair the players in the same match/tournament
            const room = players[pairedPlayerId].room;
            players[socket.id].room = room;
            players[socket.id].nb = 2;
            players[pairedPlayerId].isWaiting = false;
            players[socket.id].id = socket.id;
            players[socket.id].position = new Vector3(-centerDistanceToPaddle, 0, 0);

            // Create a ball for the game
            let tmpBall = new Ball(new Vector3(0, 0, 0), new Vector3(0, 0, 0));
            tmpBall.room = room;
            balls[room] = { id: socket.id, room: room, ball: tmpBall };

            players[pairedPlayerId].ball = balls[room];
            players[socket.id].ball = balls[room];
            // Join the room for both players
            socket.join(room);
            setCookie(socket, pairedPlayerId);

            // Start the game
            startGame(room, socket.id, pairedPlayerId);
            io.to(room).emit('startGame', {
                player1: players[pairedPlayerId],
                player2: players[socket.id],
                ball: balls[room]
            });
            // console.log('PLAYERS:', players);
        } else {
            // No available player with the same match/tournament ID, make this player wait
            const room = crypto.randomUUID(); // Generate a random room ID
            players[socket.id].position = new Vector3(centerDistanceToPaddle, 0, 0);
            players[socket.id].id = socket.id;
            players[socket.id].room = room;
            players[socket.id].nb = 1;
            players[socket.id].isWaiting = true;

            socket.join(room);
        }
    }
    socket.on('userInput', (userInput) => {
        if (players[socket.id])
        {
            players[socket.id].up = userInput.up;
            players[socket.id].down = userInput.down;
        }
    });
    socket.on('disconnect', () => {
        if (players[socket.id])
        {
            console.log('disconnected')
            players[socket.id].connected = false;
            if (players[socket.id].isWaiting == true)
                delete players[socket.id]
            
        }
    // console.log('PLAYERS:', players);
    });
});

app.use(cookieParser());

// app.use(express.static(path.join()));

// app.get('/', (req, res) => {
//     res.sendFile(path.join(__dirname, 'index.html'));
// });

app.get('*', (req, res) => {
    res.send(`
      <!DOCTYPE html>
      <html>
        <head>
          <title>Socket.IO Server</title>
        </head>
        <body>
          <h1>Welcome to Socket.IO Server</h1>
          <p>WebSocket connection is handled separately!</p>
        </body>
      </html>
    `);
});

server.listen(port, '0.0.0.0', () => {
    console.log(`Server running on port ${port}`);
});

instrument(io, { auth: false });

