const express = require("express");
const querystring = require("querystring");
const cors = require("cors");
const axios = require("axios");
const app = express();
app.use(cors());
app.use(express.json());
const session = require("express-session");
const cookieParser = require("cookie-parser");
app.use(cookieParser());

app.get("/oauth", (req, res) => {
    const csrfState = Math.random().toString(36).substring(2);
    res.cookie("csrfState", csrfState, { maxAge: 60000 });
      let url = "https://www.tiktok.com/v2/auth/authorize/";
      // the following params need to be in `application/x-www-form-urlencoded` format.
      url += "?client_key=aw0h2vs3s39ad7dk";
      url += "&scope=user.info.basic,video.upload,video.publish";
      url += "&response_type=code";
      url +=
      "&redirect_uri=https://redirect-uri-tan.vercel.app/redirect";
      url += "&state=" + csrfState;
    res.json({ url: url });
  });
app.listen(4000, ()=>{console.log("server is running on port 4000") })