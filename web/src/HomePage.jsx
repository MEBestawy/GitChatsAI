import Header from "./Header";
import {useState} from "react";

const HomePage = () => {

    const [repoLink, setRepoLink] = useState('');
    const [responseMessage, setResponseMessage] = useState('');

    const handleRepoLinkChange = (event) => {
        setRepoLink(event.target.value);
    };

    const handleTrainModel = () => {
        // Make a PUT request to the API
        fetch(`${process.env.REACT_APP_REPO_MANAGER_API_URL}/parseGithubRepo?repo_link=${repoLink}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
            },
        })
            .then((response) => {
                // Check if the request was successful
                if (!response.ok) 
                    return response.json();

                window.location.href = "/chat";
            })
            .then((data) => {
                // Assuming the API returns a JSON response with a "result" field
                setResponseMessage(data.result);
            })
            .catch((error) => {
                console.error('Error:', error);
            });        
    };

    return (
        <>
            {/* <Header/> */}
            <section className="text-gray-600 body-font relative flex items-center h-screen">
                <div className="container px-5 py-26 mx-auto pb-20">
                    <div className="container mx-auto flex p-5 flex-col md:flex-row items-center justify-center">
                        <a className="flex title-font font-medium items-center text-gray-900 lg:items-center lg:justify-center mb-4 md:mb-0">
                            <svg xmlns="http://www.w3.org/2000/svg" fill="none" stroke="currentColor" strokeLinecap="round"
                                strokeLinejoin="round" strokeWidth="2"
                                className="w-16 h-16 text-white p-2 bg-indigo-500 rounded-full" viewBox="0 0 24 24">
                                <path d="M12 2L2 7l10 5 10-5-10-5zM2 17l10 5 10-5M2 12l10 5 10-5"></path>
                            </svg>
                            <span className="ml-4 text-4xl">GitChats AI</span>
                        </a>
                    </div>

                    <div className="mb-3" />

                    <div className="lg:w-1/2 md:w-2/3 mx-auto">
                        <div className="flex flex-wrap -m-2">
                            <div className="p-2 w-full">
                                <div className="relative">
                                    <label htmlFor="name" className="leading-7 text-sm text-gray-600">Github Repo</label>
                                    <input type="text" id="name" name="name"
                                           className="w-full bg-gray-100 bg-opacity-50 rounded border border-gray-300 focus:border-indigo-500 focus:bg-white focus:ring-2 focus:ring-indigo-200 text-base outline-none text-gray-700 py-1 px-3 leading-8 transition-colors duration-200 ease-in-out"
                                           onChange={handleRepoLinkChange}
                                    />
                                </div>
                            </div>

                            <div className="p-2 w-full mb-6" />

                            <div className="p-2 w-full">
                                <button
                                    className="flex mx-auto text-white bg-indigo-500 border-0 py-2 px-8 focus:outline-none hover:bg-indigo-600 rounded text-lg"
                                    onClick={handleTrainModel}
                                >
                                    Get Chatting!
                                </button>
                            </div>
                        </div>
                    </div>
                </div>
            </section>

            {responseMessage && <p>Response: {responseMessage}</p>}
        </>
    );
}

export default HomePage;