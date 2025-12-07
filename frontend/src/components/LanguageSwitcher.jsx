import React from 'react';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';
import Link from '@docusaurus/Link';

const LanguageSwitcher = ({ currentPath }) => {
  const { i18n } = useDocusaurusContext();
  const { currentLocale, locales } = i18n;

  const getTranslatedPath = (locale) => {
    // Assuming a simple path structure like /docs/en/intro or /docs/ur/intro
    // This might need more sophisticated logic for complex routing.
    const parts = currentPath.split('/');
    if (locales.includes(parts[1])) {
      parts[1] = locale;
    } else if (parts[0] === '') { // Root path case, e.g., / becomes /ur/
      parts.splice(1, 0, locale); // Insert locale after empty string for root
    }
    return parts.join('/').replace('//', '/'); // Clean up potential double slashes
  };

  return (
    <div style={{ margin: '10px 0', textAlign: 'right' }}>
      {locales.map((locale) => (
        <Link
          key={locale}
          to={getTranslatedPath(locale)}
          style={{
            marginLeft: '10px',
            fontWeight: currentLocale === locale ? 'bold' : 'normal',
            textDecoration: 'none',
            color: currentLocale === locale ? '#007bff' : '#333',
          }}
        >
          {locale.toUpperCase()}
        </Link>
      ))}
    </div>
  );
};

export default LanguageSwitcher;
