import React, { useEffect, useState } from 'react';
import TikTokCreatorInfo from './TikTokCreatorInfo';
import { Link } from 'react-router-dom';
const Home = () => {
  const [responseData, setResponseData] = useState(null);
  const [accessToken, setAccessToken] = useState('');

  useEffect(() => {
    // Parse query parameters from URL
    const params = new URLSearchParams(window.location.search);
    const responseJson = params.get('response');

    if (responseJson) {
      try {
        // Parse JSON response
        const parsedResponse = JSON.parse(decodeURIComponent(responseJson));
        setResponseData(parsedResponse);
        setAccessToken(parsedResponse.access_token); // Use parsedResponse here
        console.log(parsedResponse.access_token);    // Log the access token to check
      } catch (error) {
        console.error('Error parsing JSON:', error);
      }
    }
  }, []);

  return (
    <div className="bg-black text-white min-h-screen flex flex-col justify-center items-center">
      {responseData ? (
        <div className="text-center">
          <h3 className="text-3xl mb-4">Welcome</h3>
          <TikTokCreatorInfo accessToken={accessToken} />
          <Link to="/editor" accessToken={accessToken}>
        <button className="bg-razzmatazz text-white mt-2 py-2 px-4 rounded-lg shadow-lg hover:bg-splash transition-colors">Create</button>
       </Link>
        </div>
        ) : (
        <p>Handling TikTok Authorization...</p>
      )}
    </div>
  );
};

export default Home;
