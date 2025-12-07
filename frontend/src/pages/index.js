import Layout from '@theme/Layout';
import Link from '@docusaurus/Link';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';
import clsx from 'clsx';
import styles from './index.module.css';

export default function Home() {
  const { siteConfig } = useDocusaurusContext();

  return (
    <Layout
      title="Physical AI and Humanoid Robotics"
      description="AI-native textbook on embodied intelligence, humanoid robots, and the future of physical AI">
      
      <header className={styles.hero}>
        <div className={styles.container}>
          <h1 className={styles.title}>
            Welcome to <br />
            <span className={styles.gradientText}>Physical AI</span><br />
            and Humanoid Robotics
          </h1>
          <p className={styles.subtitle}>
            The first AI-native textbook for the era of robots that move, learn, and live in the real world
          </p>
          <div className={styles.buttons}>
            <Link to="/docs/introduction-to-physical-ai" className={clsx('button button--lg', styles.startButton)}>
             Start Reading Free
            </Link>
          </div>
        </div>
        
        {/* Beautiful robot wave */}
        <div className={styles.robot}>
          🤖
        </div>
      </header>

      {/* Quick features */}
      <section className={styles.features}>
        <div className="container">
          <div className="row">
            <div className="col col--4">
              <div className={styles.feature}>
                <span className={styles.icon}>⚡</span>
                <h3>Real-time Updated</h3>
                <p>Latest research every week — Tesla Bot, Figure 01, Atlas, and more!</p>
              </div>
            </div>
            <div className="col col--4">
              <div className={styles.feature}>
                <span className={styles.icon}>🎨</span>
                <h3>Interactive Diagrams</h3>
                <p>3D models, animations, and code you can run</p>
              </div>
            </div>
            <div className="col col--4">
              <div className={styles.feature}>
                <span className={styles.icon}>🌍</span>
                <h3>Urdu + English</h3>
                <p>Padho apni language mein — bilkul free!</p>
              </div>
            </div>
          </div>
        </div>
      </section>
    </Layout>
  );
}