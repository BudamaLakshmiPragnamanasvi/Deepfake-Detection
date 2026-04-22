import { motion } from 'framer-motion';

export default function ConfidenceBar({ label, confidence }) {
  const isFake = label === "Fake";
  const percentage = Math.round(confidence * 100);
  
  // Fake = Red (high manipulation), Real = Green (authentic)
  const colorClass = isFake ? 'bg-red-500' : 'bg-green-500';

  return (
    <div className="w-full mt-4">
      <div className="flex justify-between text-sm font-medium mb-1">
        <span className="text-gray-300">Confidence</span>
        <span className="text-white">{percentage}%</span>
      </div>
      <div className="h-3 w-full bg-gray-800 rounded-full overflow-hidden shadow-inner">
        <motion.div
          initial={{ width: 0 }}
          animate={{ width: `${percentage}%` }}
          transition={{ duration: 1, ease: "easeOut" }}
          className={`h-full ${colorClass} shadow-[0_0_10px_rgba(0,0,0,0.5)]`}
          style={{ boxShadow: isFake ? '0 0 10px #ef4444' : '0 0 10px #22c55e' }}
        />
      </div>
    </div>
  );
}
