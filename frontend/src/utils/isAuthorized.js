import axios from 'axios';
// export async function isAuthorized(ORIGIN_IP) {
// 	try {
// 		const response = await axios.get(`https://${ORIGIN_IP}:8000/api/user/is_logged_in/`);
// 		if (response.status === 200) {
// 			return true;
// 		} else {
// 			return false;
// 		}
// 	} catch (error) {
// 		console.error("Error checking login status:", error);
// 		return false;
// 	}
// }


// export async function isAuthorized(ORIGIN_IP) {
//     if (!ORIGIN_IP) {
//         console.error("Invalid IP address.");
//         return false;
//     }

//     try {
//         const url = `https://${ORIGIN_IP}:8000/api/user/is_logged_in/`;
//         const response = await axios.get(url, { timeout: 5000 }); // Added timeout
        
//         // Check for various successful response codes
//         if (response.status >= 200 && response.status < 300) {
//             return true;
//         }
        
//         return false; // Handle other status codes gracefully
//     } catch (error) {
//         console.error("Error checking login status:", error.message);
//         return false;
//     }
// }
// export async function isAuthorized(ORIGIN_IP) {
// 	return new Promise(async (resolve, reject) => {
// 		if (!ORIGIN_IP) {
// 			console.error("Invalid IP address.");
// 			return resolve(false);
// 		}

// 		try {
// 			const url = `https://${ORIGIN_IP}:8000/api/user/is_logged_in/`;
// 			const response = await axios.get(url, { timeout: 5000 }); // Added timeout
			
// 			// Check for various successful response codes
// 			if (response.status >= 200 && response.status < 300) {
// 				return resolve(true);
// 			}
			
// 			return resolve(false); // Handle other status codes gracefully
// 		} catch (error) {
// 			console.error("Error checking login status:", error.message);
// 			return resolve(false);
// 		}
// 	});
// }


export async function isAuthorized(ORIGIN_IP) {
    if (!ORIGIN_IP) {
        console.error("Invalid IP address.");
        return false; // Returning directly is sufficient here
    }

    try {
        const url = `https://${ORIGIN_IP}:8000/api/user/is_logged_in/`;
        const response = await axios.get(url, { timeout: 5000 }); // 5000 milliseconds (5 seconds) timeout
        
        // Check for various successful response codes
        if (response.status >= 200 && response.status < 300) {
            return true; // Return true if the user is logged in
        }

        return false; // Handle other status codes gracefully
    } catch (error) {
        console.error("Error checking login status:", error.message);
        return false; // Return false on error
    }

}

export async function isUsernameLocalStorage() {
    if (localStorage.getItem("username") === null || localStorage.getItem("username") === "" || localStorage.getItem("username") === undefined) {
        return false;
    }
    return true;
}


export async function checkUser(ORIGIN_IP) {
    if (!ORIGIN_IP) {
        console.error("Invalid IP address.");
        return false; // Returning directly is sufficient here
    }

    try {
        const response = await axios.post(`https://${ORIGIN_IP}:8000/api/user/check_user/`, { username: localStorage.getItem("username") });
        
        // Ensure response structure is correct
        const is_same = response.data.data.is_same;

        if (is_same === true) {
            return true;
        }
        return false;

    } catch (error) {
        console.error("Error checking login status:", error.message);
        return false;
    }
    
}

