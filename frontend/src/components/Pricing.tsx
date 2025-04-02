import { motion } from "framer-motion";
import { useInView } from "react-intersection-observer";
import { CheckIcon } from "@heroicons/react/24/outline";

const plans = [
  {
    name: "Basic",
    price: "Free",
    description: "Perfect for getting started with P2P trading",
    features: [
      "Up to 5 active listings",
      "Basic escrow service",
      "Email support",
      "Standard verification",
    ],
    cta: "Get Started",
    popular: false,
  },
  {
    name: "Pro",
    price: "$9.99",
    period: "per month",
    description: "For active traders who need more features",
    features: [
      "Unlimited active listings",
      "Priority escrow service",
      "24/7 chat support",
      "Advanced verification",
      "Lower trading fees",
      "Analytics dashboard",
    ],
    cta: "Subscribe Now",
    popular: true,
  },
  {
    name: "Enterprise",
    price: "Custom",
    description: "For businesses and high-volume traders",
    features: [
      "Custom solutions",
      "Dedicated account manager",
      "API access",
      "White-label options",
      "Custom integrations",
      "SLA guarantees",
    ],
    cta: "Contact Sales",
    popular: false,
  },
];

const Pricing = () => {
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
    <section id="pricing" className="py-20 bg-background-dark">
      <div className="container mx-auto px-4">
        <div className="text-center mb-16">
          <h2 className="text-3xl md:text-4xl font-bold mb-4 text-text">
            Simple, Transparent Pricing
          </h2>
          <p className="text-text-light max-w-2xl mx-auto">
            Choose the plan that works best for your trading needs. All plans
            include our core escrow service to ensure secure transactions.
          </p>
        </div>

        <motion.div
          ref={ref}
          variants={containerVariants}
          initial="hidden"
          animate={inView ? "visible" : "hidden"}
          className="grid grid-cols-1 md:grid-cols-3 gap-8"
        >
          {plans.map((plan) => (
            <motion.div
              key={plan.name}
              variants={itemVariants}
              className={`glossy-card p-8 flex flex-col ${
                plan.popular ? "border-2 border-primary shadow-lg relative" : ""
              }`}
            >
              {plan.popular && (
                <div className="absolute -top-4 left-1/2 -translate-x-1/2 bg-primary text-white px-4 py-1 rounded-full text-sm font-medium">
                  Most Popular
                </div>
              )}
              <div className="mb-6">
                <h3 className="text-2xl font-bold text-text mb-2">
                  {plan.name}
                </h3>
                <div className="flex items-baseline mb-2">
                  <span className="text-4xl font-bold text-text">
                    {plan.price}
                  </span>
                  {plan.period && (
                    <span className="text-text-light ml-2">{plan.period}</span>
                  )}
                </div>
                <p className="text-text-light">{plan.description}</p>
              </div>
              <ul className="space-y-3 mb-8 flex-grow">
                {plan.features.map((feature) => (
                  <li key={feature} className="flex items-start">
                    <CheckIcon className="h-5 w-5 text-primary mr-2 flex-shrink-0 mt-0.5" />
                    <span className="text-text-light">{feature}</span>
                  </li>
                ))}
              </ul>
              <button
                className={`w-full py-3 rounded-lg font-medium transition-colors ${
                  plan.popular
                    ? "bg-primary hover:bg-primary-dark text-white"
                    : "bg-secondary/10 hover:bg-secondary/20 text-secondary"
                }`}
              >
                {plan.cta}
              </button>
            </motion.div>
          ))}
        </motion.div>

        <div className="text-center mt-12">
          <p className="text-text-light mb-4">
            Have questions about our pricing?{" "}
            <a href="#faq" className="text-primary hover:underline">
              Check our FAQ
            </a>{" "}
            or{" "}
            <a href="#" className="text-primary hover:underline">
              contact our support team
            </a>
            .
          </p>
        </div>
      </div>
    </section>
  );
};

export default Pricing;
