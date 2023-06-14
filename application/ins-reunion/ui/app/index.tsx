import ReactDOM from 'react-dom';
import React from 'react';
import PFPageManager from "@pfo/pf-react/src/artifacts/manager/pf-page-manager";
import AppRegistry from "./config/app-registry";


const registry = new AppRegistry();
ReactDOM.render(<PFPageManager
    appConfig={registry.getAppConfig()}
    urlMapping={registry.getURLMapping()}
    contextProps={registry.getContextProps()}
/>, document.getElementById('bismillah-sw'));