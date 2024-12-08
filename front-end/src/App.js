import React, { useState } from 'react';
import { AlertCircle } from 'lucide-react';
import './App.css';

// Predefined login credentials
const VALID_USERS = [
  { email: 'user1@example.com', password: 'pass1', role: 'Role 1' },
  { email: 'user2@example.com', password: 'pass2', role: 'Role 2' },
  { email: 'user3@example.com', password: 'pass3', role: 'Role 3' }
];

// Custom Alert component
const CustomAlert = ({ variant = 'default', children }) => {
  const className = variant === 'destructive' ? 'alert alert-error' : 'alert alert-info';
  return (
    <div className={className}>
      {children}
    </div>
  );
};

const LoginPage = ({ onLogin }) => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');

  const handleLogin = (e) => {
    e.preventDefault();
    const user = VALID_USERS.find(u => u.email === email && u.password === password);
    if (user) {
      onLogin(user);
    } else {
      setError('Invalid email or password');
    }
  };

  return (
    <div className="login-container">
      <div className="login-box">
        <h2>Please Login first!</h2>
        <form onSubmit={handleLogin} className="login-form">
          <div className="form-group">
            <label>Email</label>
            <input
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
            />
          </div>
          <div className="form-group">
            <label>Password</label>
            <input
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
            />
          </div>
          {error && (
            <CustomAlert variant="destructive">
              <AlertCircle className="alert-icon" />
              <span>{error}</span>
            </CustomAlert>
          )}
          <button type="submit" className="btn btn-primary">
            Login
          </button>
        </form>
      </div>
    </div>
  );
};

const RolePage = ({ user, onLogout }) => {
  const [rollNumber, setRollNumber] = useState('');
  const [entryType, setEntryType] = useState('HOME');
  const [submitted, setSubmitted] = useState(false);
  const [message, setMessage] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (rollNumber.length !== 8) {
      setMessage('Please enter a valid Roll Number');
      setSubmitted(false);
      return;
    }

    setIsLoading(true);

    try {
      const response = await fetch('http://127.0.0.1:5000/submit-form', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          // make changes here
          roll_number: rollNumber,
          parameter1: entryType,
          parameter2: user.role,
        }),
      });

      const data = await response.json();
      
      // if data returned will be -1 for first entry and  pop up will have details accordingly
      // if data returned is ! -1 means second entry

      if (data.success) {
        setSubmitted(true);
        setMessage(`Entry registered for Roll Number ${rollNumber}`);
        setRollNumber(''); // Clear the input after successful submission
        setEntryType('');
      } else {
        setSubmitted(false);
        setMessage('Error recording entry. Please try again.');
      }
    } catch (error) {
      setSubmitted(false);
      setMessage('Error connecting to server. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };

  const isUser1OrUser2 = user.email === 'user1@example.com' || user.email === 'user2@example.com';

  return (
    <div className="role-container">
      <div className="role-header">
        <h1>{user.role} Dashboard</h1>
        <button onClick={onLogout} className="btn btn-danger">
          Logout
        </button>
      </div>
      <div className="role-content">
        <div className="role-box">
          <form onSubmit={handleSubmit} className="role-form">
            <div className="form-group">
              <label>Enter Roll Number</label>
              <input
                type="text"
                value={rollNumber}
                onChange={(e) => setRollNumber(e.target.value)}
                required
                maxLength={8}
              />
            </div>

            {isUser1OrUser2 && rollNumber.length === 8 && (
              <div className="entry">
                <button
                  type="button" // Changed to type="button" to prevent form submission
                  className={`type-btn ${entryType === 'market' ? 'active' : ''}`}
                  onClick={() => setEntryType('market')}
                >
                  Market
                </button>
                <button
                  type="button" // Changed to type="button" to prevent form submission
                  className={`type-btn ${entryType === 'home' ? 'active' : ''}`}
                  onClick={() => setEntryType('home')}
                >
                  Home
                </button>
              </div>
            )}

            <button 
              type="submit" 
              className="btn btn-primary btn-success"
              disabled={isLoading || (isUser1OrUser2 && !entryType)}
            >
              {isLoading ? 'Submitting...' : 'Submit'}
            </button>
          </form>
          
          {message && (
            <CustomAlert variant={submitted ? 'default' : 'destructive'}>
              <span>{message}</span>
            </CustomAlert>
          )}
        </div>
      </div>
    </div>
  );
};

// const RolePage = ({ user, onLogout }) => {
//   const [rollNumber, setRollNumber] = useState('');
//   const [entryType, setEntryType] = useState('');
//   const [submitted, setSubmitted] = useState(false);

//   const handleSubmit = (e) => {
//     e.preventDefault();
//     (rollNumber.length <8 ) ? setSubmitted(false) : setSubmitted(true);
//   };

//   const isUser1OrUser2 = user.email === 'user1@example.com' || user.email === 'user2@example.com';

//   return (
//     <div className="role-container">
//       <div className="role-header">
//         <h1>{user.role} Dashboard</h1>
//         <button onClick={onLogout} className="btn btn-danger">
//           Logout
//         </button>
//       </div>
//       <div className="role-content">
//         <div className="role-box">
//           <form onSubmit={handleSubmit} className="role-form">
//             <div className="form-group">
//               <label>Enter Roll Number</label>
//               <input
//                 type="text"
//                 value={rollNumber}
//                 onChange={(e) => setRollNumber(e.target.value)}
//                 required
//               />
//             </div>

//             {/* add location constraint */}
//             {isUser1OrUser2 && rollNumber.length === 8 && (
//               <div className="entry">
//                 <button
//                   type="submit"
//                   className="type-btn"
//                   onClick={() => setEntryType('market')}
//                 >
//                   Market
//                 </button>
//                 <button
//                   type="submit"
//                   className="type-btn"
//                   onClick={() => setEntryType('home')}
//                 >
//                   Home
//                 </button>
//               </div>
//             )}

//             <button type="submit" className="btn btn-primary btn-success">
//               Submit
//             </button>
//           </form>
//           {(submitted && rollNumber) ? (
//             <CustomAlert>
//             <span>Please enter a valid Roll Number</span>
//           </CustomAlert>
//           ) : (
//             <CustomAlert>
//               <span>Entry registered for Roll Number {rollNumber}</span>
//             </CustomAlert>
//           )}
//         </div>
//       </div>
//     </div>
//   );
// };

const App = () => {
  const [currentUser, setCurrentUser] = useState(null);

  const handleLogin = (user) => {
    setCurrentUser(user);
  };

  const handleLogout = () => {
    setCurrentUser(null);
  };

  return (
    <div>
      {currentUser ? (
        <RolePage user={currentUser} onLogout={handleLogout} />
      ) : (
        <LoginPage onLogin={handleLogin} />
      )}
    </div>
  );
};

export default App;