import express, { Request, Response } from "express";
import dotenv from "dotenv";
import expressWs from "express-ws";
import { randActivity } from "./neural-net";

const { app } = expressWs(express());
dotenv.config();
const port = process.env.PORT;

// register an endpoint for our web server
app.get("/", (req: Request, res: Response) => {
  res.send("Hello, World!");

  // every 600ms, emit an event containing the simulated network activity
  setInterval(() => {
    app.emit("new-activity", { area1: randActivity() });
  }, 600);
});

app.on("new-activity", (msg) => {
  console.log("Received new activity!");
});

// run the web server
app.listen(port, () => {
  console.log(`⚡️[server]: Server is running at http://localhost:${port}`);
});
