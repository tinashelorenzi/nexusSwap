import { motion } from "framer-motion";
import { useInView } from "react-intersection-observer";
import {
  UserPlusIcon,
  DocumentTextIcon,
  ShieldCheckIcon,
  CheckCircleIcon,
} from "@heroicons/react/24/outline";

const steps = [
  {
    name: "Create an Account",
    description:
      "Sign up for a NexusSwap account in minutes. Complete the verification process to unlock all features.",
    icon: UserPlusIcon,
  },
  {
    name: "List Your Offer",
    description:
      "Create a listing with your preferred payment methods, rates, and trading limits.",
    icon: DocumentTextIcon,
  },
  {
    name: "Secure Escrow",
    description:
      "When a trade is initiated, funds are held securely in escrow until both parties fulfill their obligations.",
    icon: ShieldCheckIcon,
  },
  {
    name: "Complete Trade",
    description:
      "Once both parties confirm, the escrow is released, and the trade is completed successfully.",
    icon: CheckCircleIcon,
  },
];

const HowItWorks = () => {
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
    <section id="how-it-works" className="py-20">
      <div className="container mx-auto px-4">
        <div className="text-center mb-16">
          <h2 className="text-3xl md:text-4xl font-bold mb-4 text-text">
            How NexusSwap Works
          </h2>
          <p className="text-text-light max-w-2xl mx-auto">
            Our platform makes peer-to-peer trading simple and secure with a
            straightforward process designed to protect all parties involved.
          </p>
        </div>

        <motion.div
          ref={ref}
          variants={containerVariants}
          initial="hidden"
          animate={inView ? "visible" : "hidden"}
          className="relative"
        >
          {/* Connection line */}
          <div className="hidden md:block absolute top-1/2 left-0 right-0 h-0.5 bg-gradient-to-r from-primary/20 via-secondary/20 to-primary/20 -translate-y-1/2" />

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
            {steps.map((step, index) => (
              <motion.div
                key={step.name}
                variants={itemVariants}
                className="relative"
              >
                <div className="glossy-card p-6 text-center h-full">
                  <div className="flex justify-center mb-4">
                    <div className="p-3 rounded-full bg-primary/10 text-primary">
                      <step.icon className="h-8 w-8" />
                    </div>
                  </div>
                  <div className="hidden md:block absolute -top-4 left-1/2 -translate-x-1/2 w-8 h-8 rounded-full bg-white border-2 border-primary flex items-center justify-center text-primary font-bold">
                    {index + 1}
                  </div>
                  <h3 className="text-xl font-semibold mb-2 text-text">
                    {step.name}
                  </h3>
                  <p className="text-text-light">{step.description}</p>
                </div>
              </motion.div>
            ))}
          </div>
        </motion.div>

        <div className="text-center mt-12">
          <button className="btn-primary">Get Started Now</button>
        </div>
      </div>
    </section>
  );
};

export default HowItWorks;
