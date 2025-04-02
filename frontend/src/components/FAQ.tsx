import { useState } from "react";
import { motion } from "framer-motion";
import { useInView } from "react-intersection-observer";
import { ChevronDownIcon } from "@heroicons/react/24/outline";

const faqs = [
  {
    question: "What is NexusSwap?",
    answer:
      "NexusSwap is a peer-to-peer trading platform that provides a secure escrow service for transactions between buyers and sellers. Our platform ensures that both parties fulfill their obligations before funds are released.",
  },
  {
    question: "How does the escrow service work?",
    answer:
      "When a trade is initiated, the buyer's funds are held securely in our escrow system. Once the seller confirms delivery and the buyer verifies receipt, the funds are released to the seller. This process protects both parties from fraud and ensures safe transactions.",
  },
  {
    question: "What payment methods are supported?",
    answer:
      "NexusSwap supports a wide range of payment methods including bank transfers, digital wallets, and cryptocurrencies. Each listing specifies the accepted payment methods, allowing you to choose the most convenient option for your trade.",
  },
  {
    question: "Is NexusSwap regulated?",
    answer:
      "Yes, NexusSwap operates in compliance with relevant financial regulations. We implement strict KYC/AML procedures to ensure a safe trading environment for all users.",
  },
  {
    question: "How secure is my data and funds?",
    answer:
      "We employ industry-standard security measures including encryption, secure servers, and multi-factor authentication to protect your data and funds. Our platform undergoes regular security audits to maintain the highest standards of protection.",
  },
  {
    question: "What are the trading fees?",
    answer:
      "Our fee structure is transparent and varies by plan. The Basic plan is free to use with standard fees, while Pro and Enterprise plans offer reduced fees and additional benefits. All fees are clearly displayed before completing a transaction.",
  },
  {
    question: "How do I get started?",
    answer:
      "Getting started is easy! Simply create an account, complete the verification process, and you can begin listing offers or responding to existing listings. Our intuitive interface guides you through each step of the trading process.",
  },
  {
    question: "What happens if there's a dispute?",
    answer:
      "In case of a dispute, our dedicated support team will review the transaction details and communication between parties. We have a fair dispute resolution process to ensure both parties are treated equitably.",
  },
];

const FAQ = () => {
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
    <section id="faq" className="py-20">
      <div className="container mx-auto px-4">
        <div className="text-center mb-16">
          <h2 className="text-3xl md:text-4xl font-bold mb-4 text-text">
            Frequently Asked Questions
          </h2>
          <p className="text-text-light max-w-2xl mx-auto">
            Find answers to common questions about our platform, services, and
            trading process.
          </p>
        </div>

        <motion.div
          ref={ref}
          variants={containerVariants}
          initial="hidden"
          animate={inView ? "visible" : "hidden"}
          className="max-w-3xl mx-auto"
        >
          <div className="space-y-4">
            {faqs.map((faq, index) => (
              <FAQItem
                key={index}
                question={faq.question}
                answer={faq.answer}
                itemVariants={itemVariants}
              />
            ))}
          </div>
        </motion.div>

        <div className="text-center mt-12">
          <p className="text-text-light mb-4">
            Still have questions? Our support team is here to help.
          </p>
          <button className="btn-primary">Contact Support</button>
        </div>
      </div>
    </section>
  );
};

interface FAQItemProps {
  question: string;
  answer: string;
  itemVariants: {
    hidden: { y: number; opacity: number };
    visible: { y: number; opacity: number; transition: { duration: number } };
  };
}

const FAQItem = ({ question, answer, itemVariants }: FAQItemProps) => {
  const [isOpen, setIsOpen] = useState(false);

  return (
    <motion.div variants={itemVariants} className="glossy-card overflow-hidden">
      <button
        className="w-full flex justify-between items-center p-6 text-left"
        onClick={() => setIsOpen(!isOpen)}
      >
        <span className="font-semibold text-text">{question}</span>
        <ChevronDownIcon
          className={`h-5 w-5 text-primary transition-transform ${
            isOpen ? "transform rotate-180" : ""
          }`}
        />
      </button>
      <motion.div
        initial={false}
        animate={{ height: isOpen ? "auto" : 0 }}
        className="overflow-hidden"
      >
        <div className="p-6 pt-0 text-text-light">{answer}</div>
      </motion.div>
    </motion.div>
  );
};

export default FAQ;
