import { bootstrapApplication } from '@angular/platform-browser';
import { appConfig } from './app/app.config';
import { App } from './app/app';

// Imports from firebase
import { initializeApp } from 'firebase/app';
import { environment } from './environments/environment';

const firebaseApp = initializeApp(environment.firebaseConfig);
console.log('Firebase initialized:', firebaseApp);
export { firebaseApp };

bootstrapApplication(App, appConfig)
  .catch((err) => console.error(err));
