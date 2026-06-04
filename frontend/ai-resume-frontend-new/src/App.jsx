import React, { useState } from "react";
import { motion } from "framer-motion";

export default function App() {
  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(false);
  const [darkMode, setDarkMode] = useState(false);
  const [result, setResult] = useState(null);
  const [jobDesc, setJobDesc] = useState("");
  const [showResult, setShowResult] = useState(false);
  const [error, setError] = useState("");

  const radius = 50;
  const circumference = 2 * Math.PI * radius;
  const progress = result?.score || 0;
  const offset = circumference - (progress / 100) * circumference;

  return (
    <div
      className={`min-h-screen transition duration-500 ${
        darkMode
          ? "bg-gradient-to-br from-gray-950 via-gray-900 to-gray-800 text-gray-100"
          : "bg-gradient-to-br from-purple-200 via-pink-100 to-blue-200 text-gray-900"
      }`}
    >
      {/* NAVBAR */}
      <div className="flex justify-between items-center p-4 bg-white/80 dark:bg-gray-900/80 shadow">
        <h1 className="text-xl font-bold text-blue-600 dark:text-blue-400">
          AI Resume Analyzer
        </h1>

        <button
          onClick={() => setDarkMode(!darkMode)}
          className="px-4 py-1 rounded bg-gray-200 dark:bg-gray-700 text-black dark:text-white"
        >
          {darkMode ? "Light" : "Dark"}
        </button>
      </div>

      {/* HERO */}
      <div className="text-center mt-10">
        <h2 className="text-4xl font-bold text-blue-700 dark:text-blue-400">
          AI Resume Analyzer
        </h2>
        <p className="mt-3 text-gray-700 dark:text-gray-300">
          Upload your resume & get AI insights
        </p>
      </div>

      {/* UPLOAD */}
      <div className="mt-10 flex justify-center px-4">
        <div className="w-full max-w-xl p-6 rounded-xl bg-white/70 dark:bg-gray-900/70 shadow">

          <input
            type="file"
            onChange={(e) => setFile(e.target.files[0])}
            className="text-black dark:text-white"
          />

          <textarea
            placeholder="Enter Job Role (e.g., Backend Developer, Data Analyst)"
            className="w-full mt-4 p-3 rounded bg-white text-black dark:bg-gray-800 dark:text-white dark:placeholder-gray-400"
            onChange={(e) => setJobDesc(e.target.value)}
          />

          {/* ERROR MESSAGE */}
          {error && (
            <p className="text-red-500 mt-2 text-sm">{error}</p>
          )}

          <motion.button
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.9 }}
            onClick={async () => {

              setError("");

              // ✅ Only basic validation
              if (!file) {
                setError("Please upload resume");
                return;
              }

              if (!jobDesc || jobDesc.trim().length === 0) {
                setError("Please enter a job role");
                return;
              }

              setLoading(true);

              const formData = new FormData();
              formData.append("resume", file);
              formData.append("job_description", jobDesc);

              try {
                const res = await fetch("https://ai-resume-analyzer-production-3974.up.railway.app/analyze", {
                  method: "POST",
                  body: formData,
                });

                const data = await res.json();

                if (!res.ok) {
                  setError(data.error || "Server error");
                  setLoading(false);
                  return;
                }

                setResult(data);
                setShowResult(true);

              } catch (err) {
                console.error(err);
                setError("Cannot connect to backend");
              }

              setLoading(false);
            }}
            className="mt-4 w-full bg-green-500 text-white py-2 rounded"
          >
            {loading ? "Analyzing..." : "Analyze"}
          </motion.button>
        </div>
      </div>

      {/* RESULTS */}
      {showResult && (
        <div className="mt-16 px-6 grid grid-cols-1 md:grid-cols-2 gap-6">

          {/* SCORE */}
          <motion.div
            initial={{ scale: 0 }}
            animate={{ scale: 1 }}
            className="p-6 bg-white/70 dark:bg-gray-900/70 rounded-xl text-center"
          >
            <h3 className="text-lg font-semibold mb-4 text-blue-700 dark:text-blue-400">
              Resume Score
            </h3>

            <div className="flex justify-center relative">
              <svg width="140" height="140">
                <circle cx="70" cy="70" r={radius} stroke="#e5e7eb" strokeWidth="10" fill="none" />
                <motion.circle
                  cx="70"
                  cy="70"
                  r={radius}
                  stroke="#22c55e"
                  strokeWidth="10"
                  fill="none"
                  strokeDasharray={circumference}
                  strokeDashoffset={offset}
                  strokeLinecap="round"
                  initial={{ strokeDashoffset: circumference }}
                  animate={{ strokeDashoffset: offset }}
                  transition={{ duration: 1 }}
                />
              </svg>

              <div className="absolute top-12 text-2xl font-bold text-green-500">
                {progress}%
              </div>
            </div>
          </motion.div>

          {/* MATCHED SKILLS */}
          <motion.div className="p-6 bg-white/70 dark:bg-gray-900/70 rounded-xl">
            <h3 className="font-semibold mb-3 text-blue-700 dark:text-blue-400">
              Relevant Skills
            </h3>

            <div className="flex flex-wrap gap-2">
              {result?.matched_skills?.map((skill, i) => (
                <span
                  key={i}
                  className="px-3 py-1 bg-green-200 text-green-900 dark:bg-green-700 dark:text-white rounded-full text-sm"
                >
                  {skill}
                </span>
              ))}
            </div>
          </motion.div>

          {/* MISSING SKILLS */}
          <motion.div className="p-6 bg-white/70 dark:bg-gray-900/70 rounded-xl">
            <h3 className="font-semibold mb-3 text-blue-700 dark:text-blue-400">
              Missing Skills
            </h3>

            <div className="flex flex-wrap gap-2">
              {result?.missing_skills?.map((s, i) => (
                <span
                  key={i}
                  className="px-3 py-1 bg-red-200 text-red-900 dark:bg-red-700 dark:text-white rounded-full text-sm"
                >
                  {s}
                </span>
              ))}
            </div>
          </motion.div>

          {/* SUGGESTIONS */}
          <motion.div className="p-6 bg-white/70 dark:bg-gray-900/70 rounded-xl">
            <h3 className="font-semibold mb-3 text-blue-700 dark:text-blue-400">
              Suggestions
            </h3>

            <ul className="list-disc ml-5 text-gray-800 dark:text-gray-200">
              {result?.suggestions?.map((s, i) => (
                <li key={i}>{s}</li>
              ))}
            </ul>
          </motion.div>

        </div>
      )}
    </div>
  );
}