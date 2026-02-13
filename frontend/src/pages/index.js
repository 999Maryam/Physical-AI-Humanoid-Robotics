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
        {/* Animated background particles */}
        <div className={styles.particles}>
          <div className={styles.particle}></div>
          <div className={styles.particle}></div>
          <div className={styles.particle}></div>
          <div className={styles.particle}></div>
          <div className={styles.particle}></div>
          <div className={styles.particle}></div>
        </div>

        <div className={styles.container}>
          <div className={styles.badge}>
            <span className={styles.badgeIcon}>✨</span>
            <span>AI-Powered Learning Platform</span>
          </div>

          <h1 className={styles.title}>
            <span className={styles.titleLine1}>Welcome to the Future of</span>
            <span className={styles.gradientText}>Physical AI</span>
            <span className={styles.titleLine2}>& Humanoid Robotics</span>
          </h1>

          <p className={styles.subtitle}>
            The first AI-native textbook for the era of robots that move, learn,
            and live in the real world. Updated weekly with latest research.
          </p>

          <div className={styles.buttons}>
            <Link to="/docs/introduction-to-physical-ai" className={clsx('button button--lg', styles.startButton)}>
              <span>Start Learning Free</span>
              <span className={styles.buttonIcon}>→</span>
            </Link>
            <Link to="/docs/introduction-to-physical-ai" className={clsx('button button--lg button--outline', styles.exploreButton)}>
              <span>Explore Courses</span>
            </Link>
          </div>

          <div className={styles.stats}>
            <div className={styles.stat}>
              <div className={styles.statNumber}>50+</div>
              <div className={styles.statLabel}>Topics</div>
            </div>
            <div className={styles.stat}>
              <div className={styles.statNumber}>2</div>
              <div className={styles.statLabel}>Languages</div>
            </div>
            <div className={styles.stat}>
              <div className={styles.statNumber}>100%</div>
              <div className={styles.statLabel}>Free</div>
            </div>
          </div>
        </div>

        {/* Floating robots */}
        <div className={styles.robotFloat}>
          <div className={styles.robot}>🤖</div>
          <div className={styles.robot}>🦾</div>
          <div className={styles.robot}>🚀</div>
        </div>
      </header>

      {/* Features Section */}
      <section className={styles.features}>
        <div className="container">
          <h2 className={styles.sectionTitle}>
            <span className={styles.sectionTitleGradient}>Why Choose Us?</span>
          </h2>
          <p className={styles.sectionSubtitle}>
            Everything you need to master Physical AI and Robotics
          </p>

          <div className="row">
            <div className="col col--4">
              <div className={styles.feature}>
                <div className={styles.iconWrapper}>
                  <span className={styles.icon}>⚡</span>
                </div>
                <h3>Real-time Updates</h3>
                <p>Latest research every week — Tesla Bot, Figure 01, Atlas, and cutting-edge AI developments!</p>
              </div>
            </div>
            <div className="col col--4">
              <div className={styles.feature}>
                <div className={styles.iconWrapper}>
                  <span className={styles.icon}>🎨</span>
                </div>
                <h3>Interactive Learning</h3>
                <p>3D models, live animations, hands-on code examples you can run and experiment with</p>
              </div>
            </div>
            <div className="col col--4">
              <div className={styles.feature}>
                <div className={styles.iconWrapper}>
                  <span className={styles.icon}>🌍</span>
                </div>
                <h3>Bilingual Content</h3>
                <p>Padho apni language mein — Complete content in both Urdu and English, bilkul free!</p>
              </div>
            </div>
          </div>

          <div className="row" style={{marginTop: '3rem'}}>
            <div className="col col--4">
              <div className={styles.feature}>
                <div className={styles.iconWrapper}>
                  <span className={styles.icon}>🎯</span>
                </div>
                <h3>Structured Path</h3>
                <p>Clear learning roadmap from basics to advanced robotics concepts</p>
              </div>
            </div>
            <div className="col col--4">
              <div className={styles.feature}>
                <div className={styles.iconWrapper}>
                  <span className={styles.icon}>💡</span>
                </div>
                <h3>Expert Content</h3>
                <p>Created by AI researchers and robotics engineers from top institutions</p>
              </div>
            </div>
            <div className="col col--4">
              <div className={styles.feature}>
                <div className={styles.iconWrapper}>
                  <span className={styles.icon}>🚀</span>
                </div>
                <h3>Future Ready</h3>
                <p>Learn the skills that will define the next decade of technology</p>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className={styles.cta}>
        <div className={styles.ctaContent}>
          <h2 className={styles.ctaTitle}>Ready to Start Your Journey?</h2>
          <p className={styles.ctaSubtitle}>
            Join thousands of learners mastering the future of robotics
          </p>
          <Link to="/docs/introduction-to-physical-ai" className={clsx('button button--lg', styles.ctaButton)}>
            Begin Learning Now
          </Link>
        </div>
      </section>
    </Layout>
  );
}