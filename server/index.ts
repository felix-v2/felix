import express, { Request, Response } from "express";
import * as http from "http";
import dotenv from "dotenv";
import { Server } from "socket.io";
import { randActivity } from "./neural-net";

dotenv.config();
const port = process.env.PORT;

const app = express();
const server = http.createServer(app);
const io = new Server(server, {
  cors: {
    origin: "http://localhost:3000",
    methods: ["GET", "POST"],
  },
});

// register an endpoint for our web server
app.get("/", (req: Request, res: Response) => {
  res.end();
});

io.on("connection", (socket) => {
  console.log("a user connected");

  socket.on("disconnect", () => {
    console.log("user disconnected");
  });

  // emit a random activity matrix to the client periodically
  setInterval(() => {
    socket.emit("new-activity", randActivity());
  }, 1000);
});

// run the web server
server.listen(port, () => {
  console.log(`⚡️[server]: Server is running at http://localhost:${port}`);
});
