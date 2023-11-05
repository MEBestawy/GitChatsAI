import React, {useEffect, useState} from 'react';

const ChatPage = () => {
    const [input, setInput] = useState('');
    const [messages, setMessages] = useState([]);
    const [repoLink, setRepoLink] = useState('')
    const [isLoading, setIsLoading] = useState(false);

    useEffect(() => {
         console.log(123);
         setRepoLink(sessionStorage.getItem('repoLink'));
         console.log(sessionStorage.getItem('repoLink'));
    }, []);

    const handleInputChange = (e) => {
        setInput(e.target.value);
    };

    const handleSendMessage = () => {
        if (input.trim() !== '') {
            const newMessage = { text: input, user: 'user' };
            messages.push(newMessage)
            setInput('');
            setIsLoading(true);

            messages.push({ text: 'Fetching Response from Bot...', user: 'bot' });

            fetch(`${process.env.REACT_APP_LLM_CHAT_API_URL}/query?query=${input}&repo_link=${repoLink}`, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json',
                }
            })
                .then((response) => response.json())
                .then((data) => {
                    const responseMessage = { text: data.message, user: 'bot' };
                    messages.pop(); // Remove the "..." placeholder
                    messages.push(responseMessage);
                })
                .catch((error) => {
                    console.error('API request error:', error);
                }).finally(() => {
                setIsLoading(false);
            });
        }
    };

    return (
        <>
            <div className="container mx-auto flex p-5 flex-col md:flex-row items-center justify-center">
                <a className="flex title-font font-medium items-center text-gray-900 lg:items-center lg:justify-center mb-4 md:mb-0">
                    <svg
                        xmlns="http://www.w3.org/2000/svg"
                        fill="none"
                        stroke="currentColor"
                        strokeLinecap="round"
                        strokeLinejoin="round"
                        strokeWidth="2"
                        className="w-16 h-16 text-white p-2 bg-indigo-500 rounded-full"
                        viewBox="0 0 24 24"
                    >
                        <path d="M12 2L2 7l10 5 10-5-10-5zM2 17l10 5 10-5M2 12l10 5 10-5"></path>
                    </svg>
                    <span className="ml-4 text-4xl">GitChats AI</span>
                </a>
            </div>
            <section className="text-gray-600 body-font">
                <div className="container px-5 py-24 mx-auto">
                    <div className="text-center mb-20">
                        <h1 className="sm:text-3xl text-2xl font-medium text-center title-font text-gray-900 mb-4">
                            {repoLink}
                        </h1>
                        <p className="text-base leading-relaxed xl:w-2/4 lg:w-3/4 mx-auto">Repo description</p>
                        <p className="text-base leading-relaxed xl:w-2/4 lg:w-3/4 mx-auto">{repoLink}</p>
                    </div>
                    <div className="w-full bg-gray-100 bg-opacity-50 rounded border border-gray-300 focus:border-indigo-500 focus:bg-white focus:ring-2 focus:ring-indigo-200
                h-72 text-base outline-none text-gray-700 py-1 px-3 resize-none leading-6 transition-colors duration-200 ease-in-out">

                        <div className="chat-box">
                            {messages.map((message, index) => (
                                <div key={index} className={`rounded-lg p-2 flex items-center ${message.user === 'bot' ? 'bg-gray-100' : ''}`}>
                                    {message.text}
                                </div>
                            ))}
                        </div>

                    </div>

                    <div className="flex mx-auto mt-16 justify-center   ">
                        <input
                            type="text"
                            className="bg-white rounded border border-gray-300 focus:border-indigo-500 focus:bg-white focus:ring-2 focus:ring-indigo-200
                            text-base outline-none text-gray-700 py-1 px-3 resize-none leading-6 transition-colors duration-200 ease-in-out"
                            placeholder="Type your message..."
                            value={input}
                            onChange={handleInputChange}
                        />
                        <button
                            className="text-white bg-indigo-500 border-0 py-2 px-8 focus:outline-none hover:bg-indigo-600 rounded text-lg ml-2"
                            onClick={handleSendMessage}
                        >
                            Send
                        </button>
                    </div>
                </div>
            </section>
        </>
    );
};

export default ChatPage;