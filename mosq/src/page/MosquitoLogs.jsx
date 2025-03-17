import React from 'react';

const MosquitoLogsModal = ({ isOpen, onClose, mosquitoName, logs }) => {
    if (!isOpen) return null;

    return (
        <div className="fixed inset-0 bg-opacity-50 flex justify-center items-center">
            <div className="bg-white p-6 rounded-lg shadow-lg max-w-md w-full">
                <h2 className="text-xl font-bold mb-4">{mosquitoName} - Detection Logs</h2>
                <ul className="space-y-2">
                    {logs.length > 0 ? (
                        logs.map((log, index) => (
                            <li key={index} className="border p-2 rounded">
                                {log.detected_time}
                            </li>
                        ))
                    ) : (
                        <p className="text-gray-500">No logs available.</p>
                    )}
                </ul>
                <button onClick={onClose} className="mt-4 px-4 py-2 bg-red-500 text-white rounded">Close</button>
            </div>
        </div>
    );
};

export default MosquitoLogsModal;
