import { motion } from "framer-motion";
import { useInView } from "react-intersection-observer";
import {
  ShieldCheckIcon,
  CurrencyDollarIcon,
  UserGroupIcon,
  ChatBubbleLeftRightIcon,
  ChartBarIcon,
  GlobeAltIcon,
} from "@heroicons/react/24/outline";

const features = [
  {
    name: "Secure Escrow",
    description:
      "Your funds are held securely in escrow until the transaction is completed, ensuring safe trading for all parties.",
    icon: ShieldCheckIcon,
  },
  {
    name: "Multiple Payment Methods",
    description:
      "Support for various payment methods including bank transfers, digital wallets, and cryptocurrencies.",
    icon: CurrencyDollarIcon,
  },
  {
    name: "Verified Users",
    description:
      "Connect with verified traders and build your reputation within our trusted community.",
    icon: UserGroupIcon,
  },
  {
    name: "24/7 Support",
    description:
      "Our dedicated support team is available around the clock to assist you with any issues.",
    icon: ChatBubbleLeftRightIcon,
  },
  {
    name: "Real-time Analytics",
    description:
      "Track your trading activity and market trends with our comprehensive analytics dashboard.",
    icon: ChartBarIcon,
  },
  {
    name: "Global Reach",
    description:
      "Trade with users from around the world, expanding your trading opportunities globally.",
    icon: GlobeAltIcon,
  },
];

const Features = () => {
  const [ref, inView] = useInView({
    triggerOnce: true,
    threshold: 0.1,
  });

  const containerVariants = {
    hidden: { opacity: 0 },
    visible: {
      opacity: 1,
      transition: {
        staggerChildren: 0.1,
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
    <section id="features" className="py-20 bg-background-dark">
      <div className="container mx-auto px-4">
        <div className="text-center mb-16">
          <h2 className="text-3xl md:text-4xl font-bold mb-4 text-text">
            Why Choose NexusSwap
          </h2>
          <p className="text-text-light max-w-2xl mx-auto">
            Our platform offers a comprehensive solution for secure peer-to-peer
            trading with features designed to protect and enhance your trading
            experience.
          </p>
        </div>

        <motion.div
          ref={ref}
          variants={containerVariants}
          initial="hidden"
          animate={inView ? "visible" : "hidden"}
          className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8"
        >
          {features.map((feature) => (
            <motion.div
              key={feature.name}
              variants={itemVariants}
              className="glossy-card p-6 hover:shadow-lg transition-shadow"
            >
              <div className="flex items-center mb-4">
                <div className="p-2 rounded-lg bg-primary/10 text-primary mr-4">
                  <feature.icon className="h-6 w-6" />
                </div>
                <h3 className="text-xl font-semibold text-text">
                  {feature.name}
                </h3>
              </div>
              <p className="text-text-light">{feature.description}</p>
            </motion.div>
          ))}
        </motion.div>
      </div>
    </section>
  );
};

export default Features;
