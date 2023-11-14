import express, { Request, Response } from "express";
import dotenv from "dotenv";
import expressWs from "express-ws";

const { app } = expressWs(express());
dotenv.config();
const port = process.env.PORT;

// generates a 2d matrix of X x Y neurons, each with a random activity value between 0 and 1
const randActivity = (
  opts: {
    neuronsX?: number;
    neuronsY?: number;
    silent?: boolean;
  } = { neuronsX: 25, neuronsY: 25 }
) => {
  return Array.from(Array(opts.neuronsX)).map(() =>
    Array.from(Array(opts.neuronsY)).map(() =>
      opts.silent ? 0 : Math.random()
    )
  );
};

app.get("/", (req: Request, res: Response) => {
  res.send("Hello, World!");

  // every 600ms, emit an event containing the simulated network activity
  setInterval(() => {
    app.emit("new-activity", { area1: randActivity() });
  }, 600);
});

app.on("new-activity", (msg) => {
  console.log(msg);
});

app.listen(port, () => {
  console.log(`⚡️[server]: Server is running at http://localhost:${port}`);
});
