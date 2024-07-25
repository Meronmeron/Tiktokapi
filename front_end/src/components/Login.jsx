import React from "react";
import axios from "axios";

const Login = () => {
  const getAuthenticationUrl = () => {
    const clientId = 'aw0h2vs3s39ad7dk'; 
    const redirectUri = 'https://redirect-uri-tan.vercel.app/redirect'; 
    const scope = 'user.info.basic,video.publish,video.upload'; 
    const state = ''; 

    const params = {
      client_key: clientId,
      response_type: 'code',
      redirect_uri: redirectUri,
      scope: scope,
      state: state
  };

    // Construct the authorization URL
    const authorizationUrl = `https://www.tiktok.com/v2/auth/authorize/?${new URLSearchParams(params)}`

    // Redirect the user to the authorization URL
    window.location.href = authorizationUrl;
  };

  return (
    <div className="flex justify-center items-center h-screen bg-black">
      <button
        onClick={getAuthenticationUrl}
        className="bg-razzmatazz text-white py-2 px-4 rounded-lg shadow-lg hover:bg-splash transition-colors"
      >
        Authenticate with TikTok
      </button>
    </div>
  );
};
export default Login;