const path = require('path');
const HtmlWebpackPlugin = require('html-webpack-plugin');
const Dotenv = require('dotenv-webpack');

module.exports = (env) => {
    return {
        entry: {
            main: './app/index.tsx'
        },
        mode: 'development',
        module: {
            rules: [
                {
                    test: /\.s[ac]ss$/i,
                    use: [
                        "style-loader",
                        "css-loader",
                        "sass-loader",
                    ],
                },
                {
                    test: /\.tsx?$/,
                    use: [
                        {
                            loader: 'ts-loader',
                            options: {
                                compilerOptions: {
                                    noEmit: false,
                                },
                            },
                        },
                    ],
                    exclude: /(node_modules|build)/
                },
                {
                    test: /\.css$/i,
                    use: ["style-loader", "css-loader"],
                },
                {
                    test: /\.(png|jpe?g|gif|svg|webp)$/,
                    loader: 'file-loader',
                    options: {
                        name: '[name].[ext]',
                    },
                },
            ]
        },
        resolve: {
            extensions: ['.tsx', '.ts', '.js', '.jsx']
        },
        output: {
            path: path.resolve(__dirname, 'build'),
            filename: '[name].[hash:8].js',
            chunkFilename: '[id].[hash:8].js',
            publicPath: '/'
        },
        optimization: {
            splitChunks: {
                cacheGroups: {
                    default: false,
                    vendors: {
                        reuseExistingChunk: true
                    },
                    vendor: {
                        name: 'vendor',
                        chunks: 'all',
                        test: /node_modules/
                    }
                }
            }
        },
        plugins: [
            new HtmlWebpackPlugin({
                title: 'Ins Reunion',
                chunksSortMode: 'none',
                template: './public/index.html',
                favicon: './public/favicon.ico',
                minify: true
            }),
            new Dotenv(
                {
                    systemvars: true,
                    path: `./../../../env/${env.pfen}.env`
                }
            )
        ],

        devServer: {
            port: 1211,
            historyApiFallback: {
                disableDotRule: true
            },
            open: true
        }
    };
}
