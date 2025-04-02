import { motion } from "framer-motion";
import { useInView } from "react-intersection-observer";

const Hero = () => {
  const [ref, inView] = useInView({
    triggerOnce: true,
    threshold: 0.1,
  });

  const containerVariants = {
    hidden: { opacity: 0 },
    visible: {
      opacity: 1,
      transition: {
        staggerChildren: 0.2,
      },
    },
  };

  const itemVariants = {
    hidden: { y: 20, opacity: 0 },
    visible: {
      y: 0,
      opacity: 1,
      transition: {
        duration: 0.5,
      },
    },
  };

  return (
    <section className="pt-32 pb-20 md:pt-40 md:pb-28">
      <motion.div
        ref={ref}
        variants={containerVariants}
        initial="hidden"
        animate={inView ? "visible" : "hidden"}
        className="text-center"
      >
        <motion.h1
          variants={itemVariants}
          className="text-4xl md:text-6xl font-bold mb-6"
        >
          <span className="bg-gradient-to-r from-primary to-secondary bg-clip-text text-transparent">
            Secure Peer-to-Peer Trading
          </span>
          <br />
          <span className="text-text">Made Simple</span>
        </motion.h1>
        <motion.p
          variants={itemVariants}
          className="text-lg md:text-xl text-text-light max-w-3xl mx-auto mb-10"
        >
          NexusSwap provides a secure escrow service for peer-to-peer trading,
          ensuring safe transactions between buyers and sellers.
        </motion.p>
        <motion.div
          variants={itemVariants}
          className="flex flex-col sm:flex-row gap-4 justify-center"
        >
          <button className="btn-primary text-lg px-8 py-3">Get Started</button>
          <button className="btn-secondary text-lg px-8 py-3">
            Learn More
          </button>
        </motion.div>
        <motion.div variants={itemVariants} className="mt-16 relative">
          <div className="glossy-card p-6 md:p-8 max-w-4xl mx-auto">
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
              <div className="text-center">
                <div className="text-3xl font-bold text-primary mb-2">100%</div>
                <div className="text-text-light">Secure Transactions</div>
              </div>
              <div className="text-center">
                <div className="text-3xl font-bold text-secondary mb-2">
                  24/7
                </div>
                <div className="text-text-light">Customer Support</div>
              </div>
              <div className="text-center">
                <div className="text-3xl font-bold text-primary mb-2">0%</div>
                <div className="text-text-light">Hidden Fees</div>
              </div>
            </div>
          </div>
        </motion.div>
      </motion.div>
    </section>
  );
};

export default Hero;
