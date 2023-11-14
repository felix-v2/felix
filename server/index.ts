import express, { Request, Response } from "express";
import dotenv from "dotenv";
import expressWs from "express-ws";

const { app } = expressWs(express());
dotenv.config();
const port = process.env.PORT;

app.get("/", (req: Request, res: Response) => {
  app.emit("message", { hello: "world" });
  res.send("Hello, World!");
});

app.on("message", (msg) => {
  console.log(msg);
});

app.listen(port, () => {
  console.log(`⚡️[server]: Server is running at http://localhost:${port}`);
});
