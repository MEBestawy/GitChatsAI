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
            .then((response) => response.json())
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
            <Header/>
            <section className="text-gray-600 body-font relative">
                <div className="container px-5 py-24 mx-auto">
                    <div className="flex flex-col text-center w-full mb-12">
                        <h1 className="sm:text-3xl text-2xl font-medium title-font mb-4 text-gray-900">Train Model</h1>
                    </div>
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

                            <div className="p-2 w-full">
                                <button
                                    className="flex mx-auto text-white bg-indigo-500 border-0 py-2 px-8 focus:outline-none hover:bg-indigo-600 rounded text-lg"
                                    onClick={handleTrainModel}
                                >
                                    Train Model
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