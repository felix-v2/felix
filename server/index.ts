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
  res.send("Hello, World!");
});

io.on("connection", (socket) => {
  console.log("a user connected");
  console.log({ randActivity: randActivity() });

  socket.on("disconnect", () => {
    console.log("user disconnected");
  });

  socket.on("start-simulation", (data) => {
    console.log(`Starting simulation with duration ${data.stepDuration}`);

    // emit a random activity matrix to the client periodically
    setInterval(() => {
      socket.emit("new-activity", {
        sensoryInput1: randActivity(),
        area1: randActivity(),
        area2: randActivity(),
        area3: randActivity(),
        area4: randActivity(),
        area5: randActivity(),
        area6: randActivity(),
        motorInput1: randActivity(),

        stepDuration: data.stepDuration,
      });
    }, data.stepDuration);
  });
});

// run the web server
server.listen(port, () => {
  console.log(`⚡️[server]: Server is running at http://localhost:${port}`);
});
