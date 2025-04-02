import { BrowserRouter as Router } from "react-router-dom";
import Navbar from "./components/Navbar";
import Hero from "./components/Hero";
import Features from "./components/Features";
import HowItWorks from "./components/HowItWorks";
import Pricing from "./components/Pricing";
import FAQ from "./components/FAQ";
import Footer from "./components/Footer";
import AnimatedBackground from "./components/AnimatedBackground";
import "./App.css";

function App() {
  return (
    <Router>
      <div className="min-h-screen bg-background">
        <AnimatedBackground />
        <Navbar />
        <main className="relative">
          <Hero />
          <Features />
          <HowItWorks />
          <Pricing />
          <FAQ />
        </main>
        <Footer />
      </div>
    </Router>
  );
}

export default App;
